import uuid
from profiles.models import Profile
from customers.models import Customer
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
import base64


def generate_code():
    return str(uuid.uuid4()).replace('-', '')[:12].upper()

def get_salesman_from_id(id):
    return Profile.objects.get(id=id).user.username

def get_customer_from_id(id):
    return Customer.objects.get(id=id)

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_chart(chart_type, df, **kwargs):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10, 4), dpi=90)
    if chart_type == '#1':
        print('bar chart')
        # plt.bar(df['transaction_id'], df['price'])
        sns.barplot(x='transaction_id', y='price', data=df)

    elif chart_type == '#2':
        print('pie chart')
        plt.pie(data=df, x='price', labels=kwargs.get('labels'))

    elif chart_type == '#3':
        print('line chart')
        plt.plot(df['transaction_id'], df['price'],
                 marker='x', color="olive", linetyle='dashed')

    else:
        print("Oooops failed to identify the chart type")

    plt.tight_layout()
    return get_graph()
