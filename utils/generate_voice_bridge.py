import random




def generate_voice_bridge():
    from notification.models import MeetUp
    voice_bridge = random.randint(10000, 99999)
    meet_up = MeetUp.objects.filter(voice_bridge=voice_bridge)
    if meet_up.exists():
        return generate_voice_bridge()
    return voice_bridge
