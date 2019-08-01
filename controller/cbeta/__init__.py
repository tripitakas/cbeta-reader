from . import view, api

views = [
    view.CbetaHandler
]

handlers = [
    api.GetMuluApi, api.SearchApi, api.PrevPageApi, api.NextPageApi, api.getImgUrlApi
]
