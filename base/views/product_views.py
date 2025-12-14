from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import status

from base.models import Product, Review, Category
from base.serializers import ProductSerializer

class ProductListView(APIView):
    def get(self, request):
        query = request.query_params.get('keyword')
        if query == None:
            query = ''

        products = Product.objects.filter(name__icontains=query).order_by('-createdAt')

        page = request.query_params.get('page')
        paginator = Paginator(products, 10)

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        if page == None:
            page = 1
        
        page = int(page)

        serializer = ProductSerializer(products, many=True)
        return Response({'products': serializer.data, 'page': page, 'pages': paginator.num_pages})

class TopProductsView(APIView):
    def get(self, request):
        products = Product.objects.filter(rating__gte=4).order_by('-rating')[0:5]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductDetailView(APIView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(_id=pk)
            serializer = ProductSerializer(product, many=False)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({'detail': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        # Admin check inside method or permission_classes mixed usage
        if not request.user.is_staff:
             return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_403_FORBIDDEN)
             
        try:
            product = Product.objects.get(_id=pk)
            data = request.data

            product.name = data['name']
            product.price = data['price']
            product.brand = data['brand']
            product.countInStock = data['countInStock']
            product.category = Category.objects.get(name=data['category']) if 'category' in data else product.category
            product.description = data['description']

            product.save()

            serializer = ProductSerializer(product, many=False)
            return Response(serializer.data)
        except Product.DoesNotExist:
             return Response({'detail': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        if not request.user.is_staff:
             return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            product = Product.objects.get(_id=pk)
            product.delete()
            return Response('Product Deleted')
        except Product.DoesNotExist:
            return Response({'detail': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


class CreateProductView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        user = request.user
        product = Product.objects.create(
            user=user,
            name='Sample Name',
            price=0,
            brand='Sample Brand',
            countInStock=0,
            category=None,
            description=''
        )
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)

class CreateProductReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        try:
            product = Product.objects.get(_id=pk)
            data = request.data

            # 1 - Review already exists
            alreadyExists = product.review_set.filter(user=user).exists()
            if alreadyExists:
                content = {'detail': 'Product already reviewed'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

            # 2 - No Rating or 0
            elif data['rating'] == 0:
                content = {'detail': 'Please select a rating'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

            # 3 - Create review
            else:
                review = Review.objects.create(
                    user=user,
                    product=product,
                    name=user.first_name,
                    rating=data['rating'],
                    comment=data['comment'],
                )

                reviews = product.review_set.all()
                product.numReviews = len(reviews)

                total = 0
                for i in reviews:
                    total += i.rating

                product.rating = total / len(reviews)
                product.save()

                return Response('Review Added')
        except Product.DoesNotExist:
            return Response({'detail': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
