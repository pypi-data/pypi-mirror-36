# coding=utf-8
# --------------------------------------------------------------------------
# Copyright © 2018 FINBOURNE TECHNOLOGY LTD
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class UpsertCorporateActionRequest(Model):
    """UpsertCorporateActionRequest.

    :param corporate_action_id:
    :type corporate_action_id: str
    :param announcement_date:
    :type announcement_date: datetime
    :param ex_date:
    :type ex_date: datetime
    :param record_date:
    :type record_date: datetime
    :param payment_date:
    :type payment_date: datetime
    :param transitions:
    :type transitions: list[~lusid.models.CorporateActionTransitionDto]
    """

    _validation = {
        'corporate_action_id': {'required': True},
        'announcement_date': {'required': True},
        'ex_date': {'required': True},
        'record_date': {'required': True},
        'payment_date': {'required': True},
        'transitions': {'required': True},
    }

    _attribute_map = {
        'corporate_action_id': {'key': 'corporateActionId', 'type': 'str'},
        'announcement_date': {'key': 'announcementDate', 'type': 'iso-8601'},
        'ex_date': {'key': 'exDate', 'type': 'iso-8601'},
        'record_date': {'key': 'recordDate', 'type': 'iso-8601'},
        'payment_date': {'key': 'paymentDate', 'type': 'iso-8601'},
        'transitions': {'key': 'transitions', 'type': '[CorporateActionTransitionDto]'},
    }

    def __init__(self, corporate_action_id, announcement_date, ex_date, record_date, payment_date, transitions):
        super(UpsertCorporateActionRequest, self).__init__()
        self.corporate_action_id = corporate_action_id
        self.announcement_date = announcement_date
        self.ex_date = ex_date
        self.record_date = record_date
        self.payment_date = payment_date
        self.transitions = transitions
