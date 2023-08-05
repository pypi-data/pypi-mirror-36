import graphene
from rescape_python_helpers import ramda as R
import graphql_jwt
from django.contrib.auth import get_user_model, get_user
from graphene import ObjectType, Schema, Float, InputObjectType, Mutation, Field
from graphene_django import DjangoObjectType
from graphene_django.debug import DjangoDebug
from graphql_jwt.decorators import login_required
from rescape_graphene.graphql_helpers.json_field_helpers import resolver, model_resolver_for_dict_field

from rescape_graphene.user.user_schema import UserType, user_fields, CreateUser, UpdateUser
from rescape_graphene.graphql_helpers.schema_helpers import allowed_query_arguments, REQUIRE, \
    merge_with_django_properties, guess_update_or_create, \
    CREATE, UPDATE, input_type_parameters_for_update_or_create, graphql_update_or_create, graphql_query, \
    input_type_fields, DENY, stringify_query_kwargs

# configuration for the builtin User modal
from sample_webapp.models import Foo

user_fields = merge_with_django_properties(UserType, dict(
    id=dict(type=graphene.String, create=DENY, update=[REQUIRE]),
    username=dict(type=graphene.String, create=[REQUIRE]),
    password=dict(type=graphene.String, create=[REQUIRE], read=DENY),
    email=dict(type=graphene.String, create=[REQUIRE]),
    is_superuser=dict(type=graphene.String),
    first_name=dict(type=graphene.String, create=REQUIRE),
    last_name=dict(type=graphene.String, create=REQUIRE),
    is_staff=dict(type=graphene.Boolean),
    is_active=dict(type=graphene.Boolean),
    date_joined=dict(type=graphene.Boolean, create=DENY, update=DENY)
))

class FooType(DjangoObjectType):
    class Meta:
        model = Foo

foo_data_fields = dict(
    example=dict(type=Float),
    # References a User stored in a blob. This tests our ability to reference Django model instance ids in json blobs
    # and resolve them correctly.
    # For simplicity we limit fields to id. Mutations can only us id, and a query doesn't need other
    # details of the user--it can query separately for that. We could offer all fields in a query only
    # version of these fields
    friend=dict(
        type=UserType,
        graphene_type=UserType,
        fields=merge_with_django_properties(UserType, dict(id=dict(create=REQUIRE))),
        type_modifier=lambda typ: Field(typ, resolver=model_resolver_for_dict_field(get_user_model()))
    ),
)

FooDataType = type(
    'FooDataType',
    (ObjectType,),
    R.map_with_obj(
        # If we have a type_modifier function, pass the type to it, otherwise simply construct the type
        lambda k, v: R.prop_or(lambda typ: typ(), 'type_modifier', v)(R.prop('type', v)),
        foo_data_fields)
)
# Modify data field to use the resolver.
# I guess there's no way to specify a resolver upon field creation, since graphene just reads the underlying
# Django model to generate the fields
FooType._meta.fields['data'] = Field(FooDataType, resolver=resolver('data'))


def feature_fields_in_graphql_geojson_format(args):
    pass


foo_fields = merge_with_django_properties(FooType, dict(
    key=dict(create=REQUIRE),
    name=dict(create=REQUIRE),
    created_at=dict(),
    updated_at=dict(),
    # This refers to the FooDataType, which is a representation of all the json fields of Foo.data
    data=dict(graphene_type=FooDataType, fields=foo_data_fields, default=lambda: dict()),
    # This is a Foreign Key. Graphene generates these relationships for us, but we need it here to
    # support our Mutation subclasses below
    # For simplicity we limit fields to id. Mutations can only us id, and a query doesn't need other
    # details of the user--it can query separately for that
    user=dict(graphene_type=UserType, fields=merge_with_django_properties(UserType, dict(id=dict(create=REQUIRE))))
))

foo_mutation_config = dict(
    class_name='Foo',
    crud={
        CREATE: 'createFoo',
        UPDATE: 'updateFoo'
    },
    resolve=guess_update_or_create
)


class UpsertFoo(Mutation):
    """
        Abstract base class for mutation
    """
    foo = Field(FooType)


    def mutate(self, info, foo_data=None):
        update_or_create_values = input_type_parameters_for_update_or_create(foo_fields, foo_data)
        foo, created = Foo.objects.update_or_create(**update_or_create_values)
        return UpsertFoo(foo=foo)


class CreateFoo(UpsertFoo):
    """
        Create Foo mutation class
    """

    class Arguments:
        foo_data = type('CreateFooInputType', (InputObjectType,),
                           input_type_fields(foo_fields, CREATE, FooType))(required=True)


class UpdateFoo(UpsertFoo):
    """
        Update Foo mutation class
    """

    class Arguments:
        foo_data = type('UpdateFooInputType', (InputObjectType,),
                           input_type_fields(foo_fields, UPDATE, FooType))(required=True)


graphql_update_or_create_foo = graphql_update_or_create(foo_mutation_config, foo_fields)
graphql_query_foos = graphql_query('foos', foo_fields)


class Query(ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')
    users = graphene.List(
        UserType,
        **allowed_query_arguments(user_fields, UserType)
    )
    user = graphene.Field(
        UserType,
        **allowed_query_arguments(user_fields, UserType)
    )
    foos = graphene.List(
        FooType,
        **allowed_query_arguments(foo_fields, FooType)
    )
    foo = graphene.Field(
        FooType,
        **allowed_query_arguments(foo_fields, FooType)
    )

    @login_required
    def resolve_user(self, info, **kwargs):
       return info.context.user

    def resolve_users(self, info, **kwargs):
        return get_user_model().objects.filter(**kwargs)

    def resolve_current_user(self, info):
        context = info.context
        user = get_user(context)
        if not user:
            raise Exception('Not logged in!')

        return user

    def resolve_foos(self, info, **kwargs):
        return Foo.objects.filter(
            **stringify_query_kwargs(Foo, kwargs)
        )

    def resolve_foo(self, info, **kwargs):
        return Foo.objects.get(**kwargs)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    create_foo = CreateFoo.Field()
    update_foo = UpdateFoo.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = Schema(query=Query, mutation=Mutation)
