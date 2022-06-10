"""Contains unit tests for the resources/query module"""

from crma_api_client.resources.query import ProjectionField, QueryResponse


def test_query_response_fields__foreach():
    """Should return a list of projected fields from the foreach lineage"""
    query_response = QueryResponse.parse_obj(
        {
            "action": "query",
            "responseId": "response-id",
            "query": "query-string",
            "responseTime": 10,
            "results": {
                "records": [{}],
                "metadata": [
                    {
                        "queryLanguage": "SAQL",
                        "lineage": {
                            "type": "foreach",
                            "projections": [
                                {
                                    "field": {
                                        "id": "q2.absolute_change",
                                        "type": "numeric",
                                    },
                                    "inputs": [{"id": "q2.absolute_change"}],
                                },
                                {
                                    "field": {
                                        "id": "q2.relative_change",
                                        "type": "numeric",
                                    },
                                    "inputs": [{"id": "q2.relative_change"}],
                                },
                                {
                                    "field": {"id": "q2.entity", "type": "string"},
                                    "inputs": [{"id": "q2.Category"}],
                                },
                                {"field": {"id": "q2.dimension", "type": "string"}},
                            ],
                        },
                    }
                ],
            },
        }
    )
    assert query_response.fields == [
        ProjectionField(id="q2.absolute_change", type="numeric"),
        ProjectionField(id="q2.relative_change", type="numeric"),
        ProjectionField(id="q2.entity", type="string"),
        ProjectionField(id="q2.dimension", type="string"),
    ]


def test_query_response_fields__union():
    """Should return a list of projected fields from the union lineage"""
    query_response = QueryResponse.parse_obj(
        {
            "action": "query",
            "responseId": "response-id",
            "query": "query-string",
            "responseTime": 10,
            "results": {
                "records": [{}],
                "metadata": [
                    {
                        "queryLanguage": "SAQL",
                        "lineage": {
                            "type": "union",
                            "inputs": [
                                {
                                    "type": "foreach",
                                    "projections": [
                                        {
                                            "field": {
                                                "id": "q2.absolute_change",
                                                "type": "numeric",
                                            },
                                            "inputs": [{"id": "q2.absolute_change"}],
                                        },
                                        {
                                            "field": {
                                                "id": "q2.relative_change",
                                                "type": "numeric",
                                            },
                                            "inputs": [{"id": "q2.relative_change"}],
                                        },
                                        {
                                            "field": {
                                                "id": "q2.entity",
                                                "type": "string",
                                            },
                                            "inputs": [{"id": "q2.Category"}],
                                        },
                                        {
                                            "field": {
                                                "id": "q2.dimension",
                                                "type": "string",
                                            }
                                        },
                                    ],
                                },
                                {
                                    "type": "foreach",
                                    "projections": [
                                        {
                                            "field": {
                                                "id": "q5.absolute_change",
                                                "type": "numeric",
                                            },
                                            "inputs": [{"id": "q5.absolute_change"}],
                                        },
                                        {
                                            "field": {
                                                "id": "q5.relative_change",
                                                "type": "numeric",
                                            },
                                            "inputs": [{"id": "q5.relative_change"}],
                                        },
                                        {
                                            "field": {
                                                "id": "q5.entity",
                                                "type": "string",
                                            },
                                            "inputs": [{"id": "q5.State"}],
                                        },
                                        {
                                            "field": {
                                                "id": "q5.dimension",
                                                "type": "string",
                                            }
                                        },
                                    ],
                                },
                            ],
                        },
                    }
                ],
            },
        }
    )
    assert query_response.fields == [
        ProjectionField(id="q2.absolute_change", type="numeric"),
        ProjectionField(id="q2.relative_change", type="numeric"),
        ProjectionField(id="q2.entity", type="string"),
        ProjectionField(id="q2.dimension", type="string"),
    ]
