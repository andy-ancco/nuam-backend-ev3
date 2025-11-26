from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["GET"])
def user_info(request):
    return Response({
        "username": request.user.username,
        "rol": request.user.rol,
        "email": request.user.email
    })
