import requests
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken
from ed_dbsync.connectors.capi import CapiClient

import logging

logger = logging.getLogger(__name__)

def refresh_frontier_token(user):
    """
    Rinnova il token di accesso per un utente autenticato via Frontier.
    
    Args:
        user: L'utente di cui rinnovare il token
        
    Returns:
        bool: True se il rinnovo è avvenuto con successo, False altrimenti
    """
    try:
        # Ottieni l'account social dell'utente per il provider Frontier
        social_account = SocialAccount.objects.get(user=user, provider='frontier')
        
        # Ottieni il token social associato
        token = SocialToken.objects.get(account=social_account)
        
        # Se il token non è scaduto o sta per scadere, non fare nulla
        if token.expires_at and token.expires_at > timezone.now() + timedelta(minutes=5):
            return True
            
        # Ottieni l'app social per Frontier
        social_app = SocialApp.objects.get(provider='frontier')
        
        # Prepara la richiesta per il refresh del token
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': token.token_secret,
            'client_id': social_app.client_id,
            'client_secret': social_app.secret,
        }
        
        # Invia la richiesta
        response = requests.post(
            'https://auth.frontierstore.net/token',
            data=data
        )
        response.raise_for_status()
        
        # Estrai i nuovi token
        token_data = response.json()
        
        # Aggiorna i token nel database
        token.token = token_data['access_token']
        token.token_secret = token_data['refresh_token']
        
        if 'expires_in' in token_data:
            token.expires_at = timezone.now() + timedelta(seconds=int(token_data['expires_in']))
            
        token.save()
        
        logger.info(f"Token rinnovato con successo per l'utente {user.username}")
        return True
        
    except SocialAccount.DoesNotExist:
        logger.error(f"L'utente {user.username} non ha un account Frontier collegato")
        return False
    except SocialToken.DoesNotExist:
        logger.error(f"Non è stato trovato alcun token per l'utente {user.username}")
        return False
    except requests.RequestException as e:
        logger.error(f"Errore durante il rinnovo del token: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Errore imprevisto durante il rinnovo del token: {str(e)}")
        return False
    
def get_cmdr_name(user):
    """
    Recupera il nome del comandante (CMDR) dall'API di Elite Dangerous.
    
    Args:
        user: L'utente per cui recuperare il nome del CMDR
        
    Returns:
        str: Il nome del CMDR se trovato, None altrimenti
    """
    try:
        
        api = CapiClient(agent=user)
        
        profile_data = api.get_profile()
        
        # Estrai il nome del comandante
        cmdr_name = profile_data.get('commander', {}).get('name')
        
        if cmdr_name:                
            return cmdr_name
        else:
            logger.warning(f"Nome CMDR non trovato nella risposta API per l'utente {user.username}")
            return None
        
    except Exception as e:
        logger.error(f"Errore imprevisto durante il recupero del nome CMDR: {str(e)}")
        return None