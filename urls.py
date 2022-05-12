from views import Index, Contacts, About

routes = {
    '/': Index(),
    '/contacts/': Contacts(),
    '/about/': About()
}