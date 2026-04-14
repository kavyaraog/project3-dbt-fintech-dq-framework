-- =============================================================================
-- Model : stg_fintech__transactions
-- Layer : staging
-- Source: STAGING.transactions_raw
-- Author: Kavya Gangadhara
-- Description:
--   Standardises raw fintech transaction data. Applies basic cleaning,
--   renames columns to business-friendly names, casts data types.
--   First quality gate in the pipeline.
-- =============================================================================

{{ config(
    materialized = 'view',
    tags         = ['staging', 'fintech']
) }}

with source as (

    select * from {{ ref('transactions_raw') }}

),

cleaned as (

    select
        transaction_id                              as transaction_id,
        customer_id                                 as customer_id,
        cast(amount as decimal(18,2))               as amount,
        upper(trim(status))                         as status,
        cast(transaction_date as date)              as transaction_date,
        lower(trim(payment_method))                 as payment_method,
        merchant_id                                 as merchant_id,
        current_timestamp()                         as _loaded_at

    from source

)

select * from cleaned