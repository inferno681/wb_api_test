import pytest
from fastapi import status
from sqlalchemy import text

from app.constants import (
    ABSENT_SUBSCRIPTION_MESSAGE,
    EXIST_SUBSCRIPTION_MESSAGE,
    SUBSCRIPTION_ACTIVATION_MESSAGE,
    SUBSCRIPTION_DEACTIVATION_MESSAGE,
)


@pytest.mark.anyio
async def test_collect_data_endpoint(
    client, collect_data_url, request_data, engine
):
    response = await client.post(collect_data_url, json=request_data)
    assert response.status_code == status.HTTP_200_OK
    async with engine.begin() as conn:
        result = await conn.execute(
            text('SELECT * FROM product WHERE artikul=211695539')
        )
    db_result = dict(result.mappings().first())

    assert db_result
    assert 'review_rating' in db_result
    assert 'created_at' in db_result
    assert 'updated_at' in db_result
    db_result['review_rating'] = float(db_result['review_rating'])
    db_result['created_at'] = db_result['created_at'].isoformat()
    db_result['updated_at'] = db_result['updated_at'].isoformat()

    assert db_result == response.json()


@pytest.mark.anyio
async def test_subscribe_endpoint(client, subscription_url, engine):
    response = await client.get(subscription_url)
    assert response.status_code == status.HTTP_200_OK
    async with engine.begin() as conn:
        result = await conn.execute(
            text('SELECT * FROM apscheduler_jobs WHERE id=\'211695539\'')
        )
    db_result = dict(result.mappings().first())
    assert (
        SUBSCRIPTION_ACTIVATION_MESSAGE.format(article=db_result['id'])
        == response.json()['message']
    )


@pytest.mark.anyio
async def test_exist_subscription(client, subscription_url):
    await client.get(subscription_url)
    response = await client.get(subscription_url)
    assert response.status_code == status.HTTP_200_OK
    assert (
        EXIST_SUBSCRIPTION_MESSAGE.format(article=211695539)
        == response.json()['message']
    )


@pytest.mark.anyio
async def test_unsubscribe_endpoint(client, subscription_url, engine):
    response = await client.get(subscription_url)
    assert response.status_code == status.HTTP_200_OK
    async with engine.begin() as conn:
        result = await conn.execute(
            text('SELECT * FROM apscheduler_jobs WHERE id=\'211695539\'')
        )
    db_result = dict(result.mappings().first())
    assert db_result
    response = await client.delete(subscription_url)
    assert response.status_code == status.HTTP_200_OK
    async with engine.begin() as conn:
        result = await conn.execute(
            text('SELECT * FROM apscheduler_jobs WHERE id=\'211695539\'')
        )
    assert not result.mappings().first()
    assert (
        SUBSCRIPTION_DEACTIVATION_MESSAGE.format(article=211695539)
        == response.json()['message']
    )


@pytest.mark.anyio
async def test_absent_subscription(client, subscription_url):
    await client.delete(subscription_url)
    response = await client.delete(subscription_url)
    assert response.status_code == status.HTTP_200_OK
    assert (
        ABSENT_SUBSCRIPTION_MESSAGE.format(article=211695539)
        == response.json()['message']
    )
