from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden
from django.core.cache import cache
from django.contrib.auth import authenticate
from datetime import datetime
import base64
import pdb

class UnauthorizedAccessMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # Solo aplicar middleware a rutas que comiencen con /api
        if not request.path.startswith('/api'):
            return None
        if not request.user.is_authenticated:
            auth_header = request.META.get('HTTP_AUTHORIZATION')
            if auth_header and auth_header.startswith('Basic'):
                # Basic Auth
                try:
                    encoded_credentials = auth_header.split(' ')[1]
                    decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
                    username, password = decoded_credentials.split(':', 1)
                    user = authenticate(username=username, password=password)
                    if user and user.is_active:
                        request.user = user
                        return None
                except Exception as e:
                    print(f"DEBUG: Error decodificando Basic Auth: {e}")
        if not request.user.is_authenticated:
            ip_address = self.get_client_ip(request)
            cache_key = f"alert_sent_{ip_address}"
            if not cache.get(cache_key):
                self.send_alert_email(request, ip_address)
                cache.set(cache_key, True, 300)  # 300 segundos = 5 minutos
            return HttpResponseForbidden("Acceso denegado. Usuario no autenticado.")
        return None

    def get_client_ip(self, request):
        """Obtiene la IP del cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def send_alert_email(self, request, ip_address):
        
        message = f"""
        Se detectó un intento de acceso no autorizado:
        • Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        • IP: {ip_address}
        • URL: {request.build_absolute_uri()}
        • User Agent: {request.META.get('HTTP_USER_AGENT', 'N/A')}
        """
        print("Enviando email de alerta...")
        print(message)

