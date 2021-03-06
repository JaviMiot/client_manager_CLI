import click
from clients.services import Client_Services
from clients.models import ClientModel


@click.group()
def clients():
    """Manages the clients lifecycle
    """
    pass


@clients.command()
@click.option('-n', '--name',
              type=str,
              prompt=True,
              help='The client name')
@click.option('-c', '--company',
              type=str,
              prompt=True,
              help='The client company')
@click.option('-e', '--email',
              type=str,
              prompt=True,
              help='The client email')
@click.option('-p', '--position',
              type=str,
              prompt=True,
              help='The client position')
@click.pass_context
def create(ctx, name, company, email, position):
    """Creates a new clients

    Args:
        ctx ([type]): [description]
        name ([type]): [description]
        company ([type]): [description]
        email ([type]): [description]
        position ([type]): [description]
    """

    client = ClientModel(name, company, email, position)
    client_Services = Client_Services(ctx.obj['clients_table'])
    client_Services.create_client(client)


@clients.command()
@click.pass_context
def list(ctx):
    """List All clients

    Args:
        ctx ([type]): [description]
    """
    client_Services = Client_Services(ctx.obj['clients_table'])
    clients = client_Services.list_clients()

    print('ID  |NAME  |COMPANY  |EMAIL  |POSITION  |')
    print('*'*100)

    for client in clients:
        click.echo('{ID}  |{NAME}  |{COMPANY}  |{EMAIL}  |{POSITION}  |'.format(
            ID=client['uid'],
            NAME=client['name'],
            COMPANY=client['company'],
            EMAIL=client['email'],
            POSITION=client['position']
        ))


@clients.command()
@click.argument('client_uid',
                type=str)
@click.pass_context
def update(ctx, client_uid):
    """Update a client

    Args:
        ctx ([type]): [description]
        client_uid ([type]): [description]
    """
    client_service = Client_Services(ctx.obj['clients_table'])
    clients_list = client_service.list_clients()

    client = [client for client in clients_list if client['uid'] == client_uid]

    if client:
        client = _update_client_flow(ClientModel(**client[0]))
        client_service.update_Client(client)
        click.echo('Client update')
    else:
        click.echo('Client not found')


def _update_client_flow(client):
    click.echo('Leave empty if you dont want to modify the value')
    client.name = click.prompt('New name: ', type=str, default=client.name)
    client.company = click.prompt(
        'New company: ', type=str, default=client.company)
    client.email = click.prompt('New email: ', type=str, default=client.email)
    client.position = click.prompt(
        'New position: ', type=str, default=client.position)

    return client


@clients.command()
@click.argument('client_uid',
                type=str)
@click.pass_context
def delete(ctx, client_uid):
    """Delete a client

    Args:
        ctx ([type]): [description]
        client_uid ([type]): [description]
    """
    client_service = Client_Services(ctx.obj['clients_table'])
    clients_list = client_service.list_clients()

    client = [client for client in clients_list if client['uid'] == client_uid]

    if client:
        client_service.deleted(ClientModel(**client[0]).to_dict())
        click.echo('Client deleted')
    else:
        click.echo('Client not was deleted')


all = clients
