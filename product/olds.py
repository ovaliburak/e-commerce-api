# class CategoryCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Category
#         fields = ['name', 'desc']

# class CategoryRetrieveSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Category
#         fields = ['name','desc', 'slug']

# class CategoryUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Category
#         fields = ['name', 'desc', 'slug']

# class CategoryDestroySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Category
#         fields = '__all__'




####ViewCategoryUp

    # def patch(self, request, *args, **kwargs):
    #     object = get_object_or_404(models.Category, slug=kwargs['slug'])
    #     serializer = self.get_serializer(object, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_200_OK)