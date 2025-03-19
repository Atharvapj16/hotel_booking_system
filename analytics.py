import pandas as pd

def revenue_trends(df):
    revenue_by_month = df.groupby([df['reservation_status_date'].dt.year, df['reservation_status_date'].dt.month])['adr'].sum()
    return revenue_by_month.reset_index(name='total_revenue').to_dict(orient='records')

def cancellation_rate(df):
    total_bookings = len(df)
    canceled_bookings = len(df[df['is_canceled'] == 1])
    return (canceled_bookings / total_bookings) * 100

def geographical_distribution(df):
    return df['country'].value_counts().reset_index(name='count').to_dict(orient='records')

def lead_time_distribution(df):
    return df['lead_time'].describe().to_dict()

def generate_insights(df):
    df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'], format='%d-%m-%Y')
    insights = {
        'revenue_trends': revenue_trends(df),
        'cancellation_rate': cancellation_rate(df),
        'geographical_distribution': geographical_distribution(df),
        'lead_time_distribution': lead_time_distribution(df)
    }
    return insights