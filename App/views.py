import os

import cv2
import numpy
import math
from django.conf import settings
from django.http import HttpResponse, FileResponse

from .models import Request


def runtext(request):
    if request.GET.get('text'):
        message = request.GET.get('text')
        path = f"{settings.MEDIA_ROOT}/" + message + ".mp4"
        width, height = 100, 100
        fps = 24
        duration = 3
        video_frames = fps*duration

        out = cv2.VideoWriter(path, cv2.VideoWriter.fourcc(*'mp4v'), fps, (width, height))
        frame = numpy.zeros((height, width, 3), dtype=numpy.uint8)
        x, y = width, height // 2

        font = cv2.FONT_HERSHEY_COMPLEX
        font_scale = 1
        font_thickness = 2
        font_color = (255, 255, 255)

        message_width = cv2.getTextSize(message, font, font_scale, font_thickness)[0][0]
        if message_width >= video_frames:
          if math.ceil(message_width/video_frames) - message_width/video_frames < 0.5:
            speed = math.ceil(message_width/video_frames)+1
          else:
            speed = math.ceil(message_width/video_frames)
        else:
          if 1 - message_width/video_frames < 0.5:
            speed = 2
          else:
            speed = 1
        
        for t in range(video_frames):
            frame.fill(0)
            x -= speed + 1
            cv2.putText(frame, message, (x, y), font, font_scale, font_color, font_thickness)
            out.write(frame)
        out.release()
        with open(path, 'rb') as f:
            file = f.read()
        os.remove(path)
        Request.objects.create(message=message)
        response = HttpResponse(file, content_type="video/mp4")
        response['Content-Disposition'] = 'inline; filename=' + message + ".mp4"
        return response
    else:
        return HttpResponse('Error - GET parameter "text" is not provided')
