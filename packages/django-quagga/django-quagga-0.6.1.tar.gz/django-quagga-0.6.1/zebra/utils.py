from __future__ import unicode_literals

from zebra.conf import options

AUDIT_RESULTS = options.ZEBRA_AUDIT_RESULTS


def audit_customer_subscription(customer, unknown=True):
    """
    Audits the provided customer's subscription against stripe and returns a pair
    that contains a boolean and a result type.

    Default result types can be found in zebra.conf.defaults and can be
    overridden in your project's settings.
    """
    if hasattr(customer, 'suspended') and customer.suspended:
        result = AUDIT_RESULTS['suspended']
    else:
        if hasattr(customer, 'subscription'):
            try:
                result = AUDIT_RESULTS[customer.subscription.status]
            except KeyError as err:
                # TODO should this be a more specific exception class?
                raise Exception("Unable to locate a result set for "
                                "subscription status {} in ZEBRA_AUDIT_RESULTS".format(err))
        else:
            result = AUDIT_RESULTS['no_subscription']
    return result
