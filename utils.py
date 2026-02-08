from datetime import datetime
from models import Material, UsageLog
from sklearn.linear_model import LinearRegression
import numpy as np


def get_low_stock():
    """
    Returns materials that are below or equal to their reorder point.
    """
    return Material.query.filter(Material.quantity <= Material.reorder_point).all()


def predict_depletion_days(material):
    """
    Predicts how many days before a material runs out using Linear Regression.
    Uses UsageLog data (date vs. remaining quantity).
    Returns:
        float: Estimated days until depletion
        None: If not enough data or stock not decreasing
    """

    try:
        # Get usage logs for this material (oldest first)
        usage_logs = UsageLog.query.filter_by(
            material_id=material.id
        ).order_by(UsageLog.date).all()

        # Need at least 3 data points for meaningful regression
        if len(usage_logs) < 3:
            return None

        dates = np.array([
            (log.date - usage_logs[0].date).days
            for log in usage_logs
        ]).reshape(-1, 1)

        # Quantities from logs
        quantities = np.array([log.remaining_quantity for log in usage_logs])

        # If all quantities are the same (no usage trend)
        if np.all(quantities == quantities[0]):
            return None

        # Fit linear regression (time vs. quantity)
        model = LinearRegression()
        model.fit(dates, quantities)

        m = model.coef_[0]       # slope
        b = model.intercept_     # y-intercept

        # If slope is positive → stock increasing, no depletion
        if m >= 0:
            return None

        # Predict day stock reaches zero: 0 = m*x + b  →  x = -b / m
        days_until_empty = -b / m
        current_day = dates[-1][0]
        days_remaining = days_until_empty - current_day

        # If prediction is negative, stock already below trend line
        if days_remaining <= 0:
            return 0

        return round(days_remaining, 1)

    except Exception as e:
        print(
            f"⚠️ Error in predict_depletion_days for material '{material.name}': {e}")
        return None
