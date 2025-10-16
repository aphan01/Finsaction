from rest_framework.views import APIView
from rest_framework.response import Response

class PingView(APIView):
    def get(self, request):
        # simple, no auth, proves DRF + routing work
        return Response({"ok": True, "data": {"pong": True}})