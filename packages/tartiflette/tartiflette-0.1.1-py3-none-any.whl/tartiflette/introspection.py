from collections import OrderedDict

from tartiflette.executors.types import Info
from tartiflette.types.argument import GraphQLArgument
from tartiflette.types.enum import GraphQLEnumType, GraphQLEnumValue
from tartiflette.types.field import GraphQLField
from tartiflette.types.input_object import GraphQLInputObjectType
from tartiflette.types.interface import GraphQLInterfaceType
from tartiflette.types.list import GraphQLList
from tartiflette.types.non_null import GraphQLNonNull
from tartiflette.types.object import GraphQLObjectType
from tartiflette.types.scalar import GraphQLScalarType
from tartiflette.types.union import GraphQLUnionType


class TypeKindEnum:
    SCALAR = "SCALAR"
    OBJECT = "OBJECT"
    INTERFACE = "INTERFACE"
    UNION = "UNION"
    ENUM = "ENUM"
    INPUT_OBJECT = "INPUT_OBJECT"
    LIST = "LIST"
    NON_NULL = "NON_NULL"

    type_to_kind = {
        GraphQLScalarType: SCALAR,
        GraphQLObjectType: OBJECT,
        GraphQLInterfaceType: INTERFACE,
        GraphQLUnionType: UNION,
        GraphQLEnumType: ENUM,
        GraphQLInputObjectType: INPUT_OBJECT,
        GraphQLList: LIST,
        GraphQLNonNull: NON_NULL,
    }


__TypeKind = GraphQLEnumType(
    name="__TypeKind",
    description="An enum describing what kind of type a given `__Type` is",
    values=[
        GraphQLEnumValue(
            TypeKindEnum.SCALAR, description="Indicates this type is a scalar."
        ),
        GraphQLEnumValue(
            TypeKindEnum.OBJECT,
            description="Indicates this type is an object. "
                        "`fields` and `interfaces` are valid fields.",
        ),
        GraphQLEnumValue(
            TypeKindEnum.INTERFACE,
            description="Indicates this type is an interface. "
                        "`fields` and `possibleTypes` are valid fields.",
        ),
        GraphQLEnumValue(
            TypeKindEnum.UNION,
            description="Indicates this type is a union. "
                        "`possibleTypes` is a valid field.",
        ),
        GraphQLEnumValue(
            TypeKindEnum.ENUM,
            description="Indicates this type is an enum. "
                        "`enumValues` is a valid field.",
        ),
        GraphQLEnumValue(
            TypeKindEnum.INPUT_OBJECT,
            description="Indicates this type is an input object. "
                        "`inputFields` is a valid field.",
        ),
        GraphQLEnumValue(
            TypeKindEnum.LIST,
            description="Indicates this type is a list. "
                        "`ofType` is a valid field.",
        ),
        GraphQLEnumValue(
            TypeKindEnum.NON_NULL,
            description="Indicates this type is a non-null. "
                        "`ofType` is a valid field.",
        ),
    ],
)


class __InputValueResolvers:
    @staticmethod
    async def type_resolver(parent, _arguments, _request_ctx, _info: Info):
        return parent.gql_type

    @staticmethod
    async def default_value_resolver(parent, _arguments, _request_ctx,
                                     _info: Info):
        return parent.default_value


__InputValue = GraphQLObjectType(
    name="__InputValue",
    description="Arguments provided to Fields or Directives and the input "
                "fields of an InputObject are represented as Input Values "
                "which describe their type  and optionally a default value.",
    fields=OrderedDict(
        [
            (
                "name",
                GraphQLField(name="name", gql_type=GraphQLNonNull("String")),
            ),
            (
                "description",
                GraphQLField(name="description", gql_type="String"),
            ),
            (
                "type",
                GraphQLField(
                    name="type",
                    gql_type=GraphQLNonNull("__Type"),
                    resolver=__InputValueResolvers.type_resolver,
                ),
            ),
            (
                "defaultValue",
                GraphQLField(
                    name="defaultValue",
                    gql_type="String",
                    resolver=__InputValueResolvers.default_value_resolver,
                ),
            ),
        ]
    ),
)

__EnumValue = GraphQLObjectType(
    name="__EnumValue",
    description="One possible value for a given Enum. Enum values are unique "
                "values, not a placeholder for a string or numeric value. "
                "However an Enum value is returned in a JSON response as "
                "a string.",
    fields=OrderedDict(
        [
            (
                "name",
                GraphQLField(name="name", gql_type=GraphQLNonNull("String")),
            ),
            (
                "description",
                GraphQLField(name="description", gql_type="String"),
            ),
        ]
    ),
)


class __FieldResolvers:
    @staticmethod
    async def type_resolver(parent, _arguments, _request_ctx, _info: Info):
        return parent.gql_type

    @staticmethod
    async def args_resolver(parent, _arguments, _request_ctx, _info: Info):
        return list(parent.arguments.values())


__Field = GraphQLObjectType(
    name="__Field",
    description="Object and Interface types are described by a list of Fields, "
                "each of which has a name, potentially a list of arguments, "
                "and a return type.",
    fields=OrderedDict(
        [
            (
                "name",
                GraphQLField(name="name", gql_type=GraphQLNonNull("String")),
            ),
            (
                "description",
                GraphQLField(
                    name="description", gql_type=GraphQLNonNull("String")
                ),
            ),
            (
                "args",
                GraphQLField(
                    name="args",
                    gql_type=GraphQLNonNull(
                        GraphQLList(GraphQLNonNull("__InputValue"))
                    ),
                    resolver=__FieldResolvers.args_resolver,
                ),
            ),
            (
                "type",
                GraphQLField(
                    name="type",
                    gql_type=GraphQLNonNull("__Type"),
                    resolver=__FieldResolvers.type_resolver,
                ),
            ),
        ]
    ),
)


class __TypeResolvers:
    @staticmethod
    async def kind_resolver(parent, _arguments, _request_ctx, _info: Info):
        try:
            return TypeKindEnum.type_to_kind[type(parent)]
        except Exception:
            return None

    @staticmethod
    async def fields_resolver(parent, _arguments, _request_ctx, _info: Info):
        try:
            return list(parent.fields.values())
        except Exception:
            return None

    @staticmethod
    async def possible_types_resolver(parent, _arguments, _request_ctx,
                                      info: Info):
        try:
            return info.schema.possible_types[parent.name]
        except Exception:
            return None

    # @staticmethod
    # async def enum_values_resolver(_request_ctx, execution_data):
    #     return execution_data.parent_result.enum_values

    # @staticmethod
    # async def input_fields_resolver(_request_ctx, execution_data):
    #     return execution_data.parent_result.input_fields

    @staticmethod
    async def of_type_resolver(parent, _arguments, _request_ctx, info: Info):
        try:
            return parent.gql_type
        except (AttributeError, TypeError):
            return None


__Type = GraphQLObjectType(
    "__Type",
    description="The fundamental unit of any GraphQL Schema is the type. "
                "There are many kinds of types in GraphQL as represented by "
                "the `__TypeKind` enum.\n\n"
                "Depending on the kind of a type, certain fields describe "
                "information about that type. Scalar types provide no "
                "information beyond a name and description, while Enum types "
                "provide their values. Object and Interface types provide the "
                "fields they describe. Abstract types, Union and Interface, "
                "provide the Object types possible at runtime. List and "
                "NonNull types compose other types.",
    fields=OrderedDict(
        [
            (
                "kind",
                GraphQLField(
                    name="kind",
                    gql_type=GraphQLNonNull("__TypeKind"),
                    resolver=__TypeResolvers.kind_resolver,
                ),
            ),
            ("name", GraphQLField(name="name", gql_type="String")),
            (
                "description",
                GraphQLField(name="description", gql_type="String"),
            ),
            (
                "fields",
                GraphQLField(
                    name="fields",
                    gql_type=GraphQLList(GraphQLNonNull("__Field")),
                    resolver=__TypeResolvers.fields_resolver,
                ),
            ),
            (
                "interfaces",
                GraphQLField(
                    name="interfaces",
                    gql_type=GraphQLList(GraphQLNonNull("__Type")),
                    # resolver=__TypeResolvers.interfaces_resolver
                ),
            ),
            (
                "possibleTypes",
                GraphQLField(
                    name="possibleTypes",
                    gql_type=GraphQLList(GraphQLNonNull("__Type")),
                    # resolver=__TypeResolvers.possible_types_resolver,
                ),
            ),
            (
                "enumValues",
                GraphQLField(
                    name="enumValues",
                    gql_type=GraphQLList(GraphQLNonNull("__EnumValue")),
                    # resolver=__TypeResolvers.enum_values_resolver,
                ),
            ),
            (
                "inputFields",
                GraphQLField(
                    name="inputFields",
                    gql_type=GraphQLList(GraphQLNonNull("__InputValue")),
                    # resolver=__TypeResolvers.input_fields_resolver,
                ),
            ),
            (
                "ofType",
                GraphQLField(
                    name="ofType",
                    gql_type="__Type",
                    resolver=__TypeResolvers.of_type_resolver,
                ),
            ),
        ]
    ),
)


class __SchemaResolvers:
    @staticmethod
    async def types_resolver(_parent, _arguments, _request_ctx, info: Info):
        return info.schema.types

    @staticmethod
    async def query_type_resolver(_parent, _arguments, _request_ctx,
                                  info: Info):
        return info.schema.types[info.schema.query_type]

    @staticmethod
    async def mutation_type_resolver(_parent, _arguments, _request_ctx,
                                     info: Info):
        return info.schema.types[info.schema.mutation_type]

    @staticmethod
    async def subscription_type_resolver(_parent, _arguments, _request_ctx,
                                         info: Info):
        return info.schema.types[
            info.schema.subscription_type
        ]


__Schema = GraphQLObjectType(
    name="__Schema",
    description="A GraphQL Schema defines the capabilities of a GraphQL "
                "server. It exposes all available types and directives on "
                "the server, as well as the entry points for query, mutation "
                "and subscription operations.",
    fields=OrderedDict(
        [
            (
                "types",
                GraphQLField(
                    name="types",
                    description="A list of all types supported by this server.",
                    gql_type=GraphQLNonNull(
                        GraphQLList(GraphQLNonNull("__Type"))
                    ),
                    resolver=__SchemaResolvers.types_resolver,
                ),
            ),
            (
                "queryType",
                GraphQLField(
                    name="queryType",
                    description="The type that query operations will be rooted at.",
                    gql_type=GraphQLNonNull("__Type"),
                    resolver=__SchemaResolvers.query_type_resolver,
                ),
            ),
            (
                "mutationType",
                GraphQLField(
                    name="mutationType",
                    description="If this server supports mutation, the type that "
                                "mutation operations will be rooted at.",
                    gql_type=GraphQLNonNull("__Type"),
                    resolver=__SchemaResolvers.mutation_type_resolver,
                ),
            ),
            (
                "subscriptionType",
                GraphQLField(
                    name="subscriptionType",
                    description="If this server support subscription, the type "
                                "that subscription operations will be rooted at.",
                    gql_type=GraphQLNonNull("__Type"),
                    resolver=__SchemaResolvers.subscription_type_resolver,
                ),
            ),
        ]
    ),
)

IntrospectionSchema = __Schema
IntrospectionType = __Type
IntrospectionTypeKind = __TypeKind
IntrospectionField = __Field
IntrospectionEnumValue = __EnumValue
IntrospectionInputValue = __InputValue


async def schema_resolver(_parent, _arguments, _request_ctx, info: Info):
    return info.schema


SchemaRootFieldDefinition = GraphQLField(
    name="__schema",
    gql_type=GraphQLNonNull("__Schema"),
    description="Access the current type schema of this server.",
    arguments={},
    resolver=schema_resolver,
)


async def type_resolver(_parent, arguments, _request_ctx, info: Info):
    typename = arguments["name"]
    gql_type = info.schema.types[typename]
    return gql_type


TypeRootFieldDefinition = GraphQLField(
    name="__type",
    gql_type="__Type",
    description="Request the type information of a single type.",
    arguments={
        "name": GraphQLArgument(name="name", gql_type=GraphQLNonNull("String"))
    },
    resolver=type_resolver,
)


async def typename_resolver(_parent, _arguments, _request_ctx, info: Info):
    return info.schema.types[type(info.schema_field)]


TypeNameRootFieldDefinition = GraphQLField(
    name="__typename",
    gql_type=GraphQLNonNull("String"),
    description="The name of the current Object type at runtime.",
    arguments={},
    resolver=type_resolver,
)
