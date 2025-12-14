from django.urls import path
from base.views import user_views as user_views
from base.views import product_views as product_views
from base.views import order_views as order_views

urlpatterns = [
    # User URLs
    path('users/login/', user_views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/register/', user_views.RegisterUserView.as_view(), name='register'),
    path('users/profile/', user_views.UserProfileView.as_view(), name='users-profile'),
    path('users/profile/update/', user_views.UserProfileView.as_view(), name='user-profile-update'),
    path('users/', user_views.UserListView.as_view(), name='users'),
    path('users/<str:pk>/', user_views.UserDetailView.as_view(), name='user'),
    path('users/update/<str:pk>/', user_views.UserDetailView.as_view(), name='user-update'),
    path('users/delete/<str:pk>/', user_views.UserDetailView.as_view(), name='user-delete'),

    # Product URLs
    path('products/', product_views.ProductListView.as_view(), name='products'),
    path('products/create/', product_views.CreateProductView.as_view(), name='product-create'),
    path('products/upload/', product_views.CreateProductView.as_view(), name='image-upload'),
    path('products/<str:pk>/reviews/', product_views.CreateProductReviewView.as_view(), name='create-review'),
    path('products/top/', product_views.TopProductsView.as_view(), name='top-products'),
    path('products/<str:pk>/', product_views.ProductDetailView.as_view(), name='product'),
    path('products/update/<str:pk>/', product_views.ProductDetailView.as_view(), name='product-update'),
    path('products/delete/<str:pk>/', product_views.ProductDetailView.as_view(), name='product-delete'),

    # Order URLs
    path('orders/add/', order_views.AddOrderItemsView.as_view(), name='orders-add'),
    path('orders/myorders/', order_views.MyOrdersView.as_view(), name='myorders'),
    path('orders/', order_views.OrderListView.as_view(), name='orders'),
    path('orders/<str:pk>/', order_views.OrderDetailView.as_view(), name='user-order'),
    path('orders/<str:pk>/pay/', order_views.PayOrderView.as_view(), name='pay'),
    path('orders/<str:pk>/deliver/', order_views.DeliverOrderView.as_view(), name='order-deliver'),
]
