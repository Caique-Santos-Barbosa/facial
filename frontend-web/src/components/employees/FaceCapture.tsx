'use client';

import { useRef, useState, useCallback } from 'react';
import { Button } from '@/components/ui/button';
import { Camera, X, Check } from 'lucide-react';
import { toast } from 'sonner';

interface FaceCaptureProps {
  onCapture: (file: File) => void;
}

export function FaceCapture({ onCapture }: FaceCaptureProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [capturedImage, setCapturedImage] = useState<string | null>(null);
  const [isStreaming, setIsStreaming] = useState(false);

  const startCamera = useCallback(async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'user', width: 640, height: 480 },
        audio: false,
      });

      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
        setStream(mediaStream);
        setIsStreaming(true);
      }
    } catch (error) {
      toast.error('Erro ao acessar câmera');
      console.error(error);
    }
  }, []);

  const stopCamera = useCallback(() => {
    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
      setStream(null);
      setIsStreaming(false);
    }
  }, [stream]);

  const capturePhoto = useCallback(() => {
    if (!videoRef.current || !canvasRef.current) return;

    const canvas = canvasRef.current;
    const video = videoRef.current;
    
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    ctx.drawImage(video, 0, 0);
    
    canvas.toBlob((blob) => {
      if (blob) {
        const file = new File([blob], 'face-capture.jpg', { type: 'image/jpeg' });
        const imageUrl = URL.createObjectURL(blob);
        
        setCapturedImage(imageUrl);
        onCapture(file);
        stopCamera();
        toast.success('Foto capturada com sucesso!');
      }
    }, 'image/jpeg', 0.95);
  }, [onCapture, stopCamera]);

  const resetCapture = useCallback(() => {
    setCapturedImage(null);
    startCamera();
  }, [startCamera]);

  return (
    <div className="space-y-4">
      <div className="relative bg-gray-900 rounded-lg overflow-hidden" style={{ aspectRatio: '4/3', maxWidth: '640px' }}>
        {!capturedImage ? (
          <>
            <video
              ref={videoRef}
              autoPlay
              playsInline
              className="w-full h-full object-cover"
            />
            <canvas ref={canvasRef} className="hidden" />
            
            {isStreaming && (
              <div className="absolute inset-0 border-4 border-green-500 rounded-lg pointer-events-none">
                <div className="absolute top-4 left-4 bg-green-500 text-white px-3 py-1 rounded-full text-sm font-medium">
                  ● Sistema ativo
                </div>
              </div>
            )}
          </>
        ) : (
          <img
            src={capturedImage}
            alt="Captured face"
            className="w-full h-full object-cover"
          />
        )}
      </div>

      <div className="flex gap-2">
        {!isStreaming && !capturedImage && (
          <Button onClick={startCamera} className="w-full">
            <Camera className="mr-2 h-4 w-4" />
            Iniciar Câmera
          </Button>
        )}

        {isStreaming && !capturedImage && (
          <>
            <Button onClick={capturePhoto} className="flex-1">
              <Check className="mr-2 h-4 w-4" />
              Capturar Foto
            </Button>
            <Button onClick={stopCamera} variant="outline">
              <X className="mr-2 h-4 w-4" />
              Cancelar
            </Button>
          </>
        )}

        {capturedImage && (
          <Button onClick={resetCapture} variant="outline" className="w-full">
            <Camera className="mr-2 h-4 w-4" />
            Tirar Nova Foto
          </Button>
        )}
      </div>
    </div>
  );
}

