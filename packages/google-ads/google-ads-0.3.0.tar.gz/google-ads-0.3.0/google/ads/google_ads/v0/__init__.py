# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

from google.ads.google_ads.v0 import types
from google.ads.google_ads.v0.services import account_budget_proposal_service_client
from google.ads.google_ads.v0.services import ad_group_ad_service_client
from google.ads.google_ads.v0.services import ad_group_bid_modifier_service_client
from google.ads.google_ads.v0.services import ad_group_criterion_service_client
from google.ads.google_ads.v0.services import ad_group_service_client
from google.ads.google_ads.v0.services import bidding_strategy_service_client
from google.ads.google_ads.v0.services import billing_setup_service_client
from google.ads.google_ads.v0.services import campaign_bid_modifier_service_client
from google.ads.google_ads.v0.services import campaign_budget_service_client
from google.ads.google_ads.v0.services import campaign_criterion_service_client
from google.ads.google_ads.v0.services import campaign_group_service_client
from google.ads.google_ads.v0.services import campaign_service_client
from google.ads.google_ads.v0.services import campaign_shared_set_service_client
from google.ads.google_ads.v0.services import change_status_service_client
from google.ads.google_ads.v0.services import conversion_action_service_client
from google.ads.google_ads.v0.services import customer_service_client
from google.ads.google_ads.v0.services import enums
from google.ads.google_ads.v0.services import geo_target_constant_service_client
from google.ads.google_ads.v0.services import google_ads_field_service_client
from google.ads.google_ads.v0.services import google_ads_service_client
from google.ads.google_ads.v0.services import keyword_view_service_client
from google.ads.google_ads.v0.services import recommendation_service_client
from google.ads.google_ads.v0.services import shared_criterion_service_client
from google.ads.google_ads.v0.services import shared_set_service_client
from google.ads.google_ads.v0.services import video_service_client
from google.ads.google_ads.v0.services.transports import account_budget_proposal_service_grpc_transport
from google.ads.google_ads.v0.services.transports import ad_group_ad_service_grpc_transport
from google.ads.google_ads.v0.services.transports import ad_group_bid_modifier_service_grpc_transport
from google.ads.google_ads.v0.services.transports import ad_group_criterion_service_grpc_transport
from google.ads.google_ads.v0.services.transports import ad_group_service_grpc_transport
from google.ads.google_ads.v0.services.transports import bidding_strategy_service_grpc_transport
from google.ads.google_ads.v0.services.transports import billing_setup_service_grpc_transport
from google.ads.google_ads.v0.services.transports import campaign_bid_modifier_service_grpc_transport
from google.ads.google_ads.v0.services.transports import campaign_budget_service_grpc_transport
from google.ads.google_ads.v0.services.transports import campaign_criterion_service_grpc_transport
from google.ads.google_ads.v0.services.transports import campaign_group_service_grpc_transport
from google.ads.google_ads.v0.services.transports import campaign_service_grpc_transport
from google.ads.google_ads.v0.services.transports import campaign_shared_set_service_grpc_transport
from google.ads.google_ads.v0.services.transports import change_status_service_grpc_transport
from google.ads.google_ads.v0.services.transports import conversion_action_service_grpc_transport
from google.ads.google_ads.v0.services.transports import customer_service_grpc_transport
from google.ads.google_ads.v0.services.transports import geo_target_constant_service_grpc_transport
from google.ads.google_ads.v0.services.transports import google_ads_field_service_grpc_transport
from google.ads.google_ads.v0.services.transports import google_ads_service_grpc_transport
from google.ads.google_ads.v0.services.transports import keyword_view_service_grpc_transport
from google.ads.google_ads.v0.services.transports import recommendation_service_grpc_transport
from google.ads.google_ads.v0.services.transports import shared_criterion_service_grpc_transport
from google.ads.google_ads.v0.services.transports import shared_set_service_grpc_transport
from google.ads.google_ads.v0.services.transports import video_service_grpc_transport


class AdGroupAdServiceClient(
    ad_group_ad_service_client.AdGroupAdServiceClient):
    __doc__ = ad_group_ad_service_client.AdGroupAdServiceClient.__doc__
    enums = enums


class AdGroupAdServiceGrpcTransport(
    ad_group_ad_service_grpc_transport.AdGroupAdServiceGrpcTransport):
    __doc__ = ad_group_ad_service_grpc_transport.AdGroupAdServiceGrpcTransport.__doc__


class AdGroupBidModifierServiceClient(
    ad_group_bid_modifier_service_client.AdGroupBidModifierServiceClient):
    __doc__ = ad_group_bid_modifier_service_client.AdGroupBidModifierServiceClient.__doc__
    enums = enums


class AdGroupBidModifierServiceGrpcTransport(
    ad_group_bid_modifier_service_grpc_transport.AdGroupBidModifierServiceGrpcTransport):
    __doc__ = ad_group_bid_modifier_service_grpc_transport.AdGroupBidModifierServiceGrpcTransport.__doc__


class AdGroupCriterionServiceClient(
    ad_group_criterion_service_client.AdGroupCriterionServiceClient):
    __doc__ = ad_group_criterion_service_client.AdGroupCriterionServiceClient.__doc__
    enums = enums


class AdGroupCriterionServiceGrpcTransport(
    ad_group_criterion_service_grpc_transport.AdGroupCriterionServiceGrpcTransport):
    __doc__ = ad_group_criterion_service_grpc_transport.AdGroupCriterionServiceGrpcTransport.__doc__


class AdGroupServiceClient(ad_group_service_client.AdGroupServiceClient):
    __doc__ = ad_group_service_client.AdGroupServiceClient.__doc__
    enums = enums


class AdGroupServiceGrpcTransport(
    ad_group_service_grpc_transport.AdGroupServiceGrpcTransport):
    __doc__ = ad_group_service_grpc_transport.AdGroupServiceGrpcTransport.__doc__


class BiddingStrategyServiceClient(
    bidding_strategy_service_client.BiddingStrategyServiceClient):
    __doc__ = bidding_strategy_service_client.BiddingStrategyServiceClient.__doc__
    enums = enums


class BiddingStrategyServiceGrpcTransport(
    bidding_strategy_service_grpc_transport.BiddingStrategyServiceGrpcTransport):
    __doc__ = bidding_strategy_service_grpc_transport.BiddingStrategyServiceGrpcTransport.__doc__


class CampaignBidModifierServiceClient(
    campaign_bid_modifier_service_client.CampaignBidModifierServiceClient):
    __doc__ = campaign_bid_modifier_service_client.CampaignBidModifierServiceClient.__doc__
    enums = enums


class CampaignBidModifierServiceGrpcTransport(
    campaign_bid_modifier_service_grpc_transport.CampaignBidModifierServiceGrpcTransport):
    __doc__ = campaign_bid_modifier_service_grpc_transport.CampaignBidModifierServiceGrpcTransport.__doc__


class CampaignBudgetServiceClient(
    campaign_budget_service_client.CampaignBudgetServiceClient):
    __doc__ = campaign_budget_service_client.CampaignBudgetServiceClient.__doc__
    enums = enums


class CampaignBudgetServiceGrpcTransport(
    campaign_budget_service_grpc_transport.CampaignBudgetServiceGrpcTransport):
    __doc__ = campaign_budget_service_grpc_transport.CampaignBudgetServiceGrpcTransport.__doc__


class CampaignCriterionServiceClient(
    campaign_criterion_service_client.CampaignCriterionServiceClient):
    __doc__ = campaign_criterion_service_client.CampaignCriterionServiceClient.__doc__
    enums = enums


class CampaignCriterionServiceGrpcTransport(
    campaign_criterion_service_grpc_transport.CampaignCriterionServiceGrpcTransport):
    __doc__ = campaign_criterion_service_grpc_transport.CampaignCriterionServiceGrpcTransport.__doc__


class CampaignGroupServiceClient(campaign_group_service_client.CampaignGroupServiceClient):
    __doc__ = campaign_group_service_client.CampaignGroupServiceClient.__doc__
    enums = enums


class CampaignGroupServiceGrpcTransport(
    campaign_group_service_grpc_transport.CampaignGroupServiceGrpcTransport):
    __doc__ = campaign_group_service_grpc_transport.CampaignGroupServiceGrpcTransport.__doc__


class CampaignServiceClient(campaign_service_client.CampaignServiceClient):
    __doc__ = campaign_service_client.CampaignServiceClient.__doc__
    enums = enums


class CampaignServiceGrpcTransport(
    campaign_service_grpc_transport.CampaignServiceGrpcTransport):
    __doc__ = campaign_service_grpc_transport.CampaignServiceGrpcTransport.__doc__


class CampaignSharedSetServiceClient(campaign_shared_set_service_client.CampaignSharedSetServiceClient):
    __doc__ = campaign_shared_set_service_client.CampaignSharedSetServiceClient.__doc__
    enums = enums


class CampaignSharedSetServiceGrpcTransport(
    campaign_shared_set_service_grpc_transport.CampaignSharedSetServiceGrpcTransport):
    __doc__ = campaign_shared_set_service_grpc_transport.CampaignSharedSetServiceGrpcTransport.__doc__


class CustomerServiceClient(customer_service_client.CustomerServiceClient):
    __doc__ = customer_service_client.CustomerServiceClient.__doc__
    enums = enums


class CustomerServiceGrpcTransport(
    customer_service_grpc_transport.CustomerServiceGrpcTransport):
    __doc__ = customer_service_grpc_transport.CustomerServiceGrpcTransport.__doc__


class GeoTargetConstantServiceClient(
    geo_target_constant_service_client.GeoTargetConstantServiceClient):
    __doc__ = geo_target_constant_service_client.GeoTargetConstantServiceClient.__doc__
    enums = enums


class GeoTargetConstantServiceGrpcTransport(
    geo_target_constant_service_grpc_transport.GeoTargetConstantServiceGrpcTransport):
    __doc__ = geo_target_constant_service_grpc_transport.GeoTargetConstantServiceGrpcTransport.__doc__


class GoogleAdsFieldServiceClient(
    google_ads_field_service_client.GoogleAdsFieldServiceClient):
    __doc__ = google_ads_field_service_client.GoogleAdsFieldServiceClient.__doc__
    enums = enums


class GoogleAdsFieldServiceGrpcTransport(
    google_ads_field_service_grpc_transport.GoogleAdsFieldServiceGrpcTransport):
    __doc__ = google_ads_field_service_grpc_transport.GoogleAdsFieldServiceGrpcTransport.__doc__


class GoogleAdsServiceClient(google_ads_service_client.GoogleAdsServiceClient):
    __doc__ = google_ads_service_client.GoogleAdsServiceClient.__doc__
    enums = enums


class GoogleAdsServiceGrpcTransport(
    google_ads_service_grpc_transport.GoogleAdsServiceGrpcTransport):
    __doc__ = google_ads_service_grpc_transport.GoogleAdsServiceGrpcTransport.__doc__


class KeywordViewServiceClient(
    keyword_view_service_client.KeywordViewServiceClient):
    __doc__ = keyword_view_service_client.KeywordViewServiceClient.__doc__
    enums = enums


class KeywordViewServiceGrpcTransport(
    keyword_view_service_grpc_transport.KeywordViewServiceGrpcTransport):
    __doc__ = keyword_view_service_grpc_transport.KeywordViewServiceGrpcTransport.__doc__


class RecommendationServiceClient(
    recommendation_service_client.RecommendationServiceClient):
    __doc__ = recommendation_service_client.RecommendationServiceClient.__doc__
    enums = enums


class RecommendationServiceGrpcTransport(
    recommendation_service_grpc_transport.RecommendationServiceGrpcTransport):
    __doc__ = recommendation_service_grpc_transport.RecommendationServiceGrpcTransport.__doc__


class SharedCriterionServiceClient(
    shared_criterion_service_client.SharedCriterionServiceClient):
    __doc__ = shared_criterion_service_client.SharedCriterionServiceClient.__doc__
    enums = enums


class SharedCriterionServiceGrpcTransport(
    shared_criterion_service_grpc_transport.SharedCriterionServiceGrpcTransport):
    __doc__ = shared_criterion_service_grpc_transport.SharedCriterionServiceGrpcTransport.__doc__


class SharedSetServiceClient(shared_set_service_client.SharedSetServiceClient):
    __doc__ = shared_set_service_client.SharedSetServiceClient.__doc__
    enums = enums


class SharedSetServiceGrpcTransport(
    shared_set_service_grpc_transport.SharedSetServiceGrpcTransport):
    __doc__ = shared_set_service_grpc_transport.SharedSetServiceGrpcTransport.__doc__

class AccountBudgetProposalServiceClient(
        account_budget_proposal_service_client.
        AccountBudgetProposalServiceClient):
    __doc__ = account_budget_proposal_service_client.AccountBudgetProposalServiceClient.__doc__
    enums = enums


class BillingSetupServiceClient(
        billing_setup_service_client.BillingSetupServiceClient):
    __doc__ = billing_setup_service_client.BillingSetupServiceClient.__doc__
    enums = enums


class ChangeStatusServiceClient(
        change_status_service_client.ChangeStatusServiceClient):
    __doc__ = change_status_service_client.ChangeStatusServiceClient.__doc__
    enums = enums


class ConversionActionServiceClient(
        conversion_action_service_client.ConversionActionServiceClient):
    __doc__ = conversion_action_service_client.ConversionActionServiceClient.__doc__
    enums = enums

class VideoServiceClient(video_service_client.VideoServiceClient):
    __doc__ = video_service_client.VideoServiceClient.__doc__
    enums = enums


class AccountBudgetProposalServiceGrpcTransport(
        account_budget_proposal_service_grpc_transport.
        AccountBudgetProposalServiceGrpcTransport):
    __doc__ = account_budget_proposal_service_grpc_transport.AccountBudgetProposalServiceGrpcTransport.__doc__
    enums = enums


class BillingSetupServiceGrpcTransport(
        billing_setup_service_grpc_transport.BillingSetupServiceGrpcTransport):
    __doc__ = billing_setup_service_grpc_transport.BillingSetupServiceGrpcTransport.__doc__
    enums = enums


class ChangeStatusServiceGrpcTransport(
        change_status_service_grpc_transport.ChangeStatusServiceGrpcTransport):
    __doc__ = change_status_service_grpc_transport.ChangeStatusServiceGrpcTransport.__doc__
    enums = enums


class ConversionActionServiceGrpcTransport(
        conversion_action_service_grpc_transport.ConversionActionServiceGrpcTransport):
    __doc__ = conversion_action_service_grpc_transport.ConversionActionServiceGrpcTransport.__doc__
    enums = enums

class VideoServiceGrpcTransport(video_service_grpc_transport.VideoServiceGrpcTransport):
    __doc__ = video_service_grpc_transport.VideoServiceGrpcTransport.__doc__
    enums = enums


__all__ = (
    'enums',
    'types',
    'AccountBudgetProposalServiceClient',
    'AdGroupAdServiceClient',
    'AdGroupBidModifierServiceClient',
    'AdGroupCriterionServiceClient',
    'AdGroupServiceClient',
    'BiddingStrategyServiceClient',
    'BillingSetupServiceClient',
    'CampaignBidModifierServiceClient',
    'CampaignBudgetServiceClient',
    'CampaignCriterionServiceClient',
    'CampaignGroupServiceClient',
    'CampaignServiceClient',
    'CampaignSharedSetServiceClient',
    'ChangeStatusServiceClient',
    'ConversionActionServiceClient',
    'CustomerServiceClient',
    'GeoTargetConstantServiceClient',
    'GoogleAdsFieldServiceClient',
    'GoogleAdsServiceClient',
    'KeywordViewServiceClient',
    'RecommendationServiceClient',
    'SharedCriterionServiceClient',
    'SharedSetServiceClient',
    'VideoServiceClient',
    'AccountBudgetProposalServiceGrpcTransport',
    'AdGroupAdServiceGrpcTransport',
    'AdGroupBidModifierServiceGrpcTransport',
    'AdGroupCriterionServiceGrpcTransport',
    'AdGroupServiceGrpcTransport',
    'BiddingStrategyServiceGrpcTransport',
    'BillingSetupServiceGrpcTransport',
    'CampaignBidModifierServiceGrpcTransport',
    'CampaignBudgetServiceGrpcTransport',
    'CampaignCriterionServiceGrpcTransport',
    'CampaignGroupServiceGrpcTransport',
    'CampaignServiceGrpcTransport',
    'CampaignSharedSetServiceGrpcTransport',
    'ChangeStatusServiceGrpcTransport',
    'ConversionActionServiceGrpcTransport',
    'CustomerServiceGrpcTransport',
    'GeoTargetConstantServiceGrpcTransport',
    'GoogleAdsFieldServiceGrpcTransport',
    'GoogleAdsServiceGrpcTransport',
    'KeywordViewServiceGrpcTransport',
    'RecommendationServiceGrpcTransport',
    'SharedCriterionServiceGrpcTransport',
    'SharedSetServiceGrpcTransport',
    'VideoServiceGrpcTransport',
)
