from rest_framework.pagination import PageNumberPagination

class MaterialsPagination(PageNumberPagination):
    page_size = 5  # количество объектов по умолчанию на странице
    page_size_query_param = 'page_size'  # параметр, чтобы пользователь мог менять размер страницы
    max_page_size = 50  # максимально допустимое количество объектов на странице
