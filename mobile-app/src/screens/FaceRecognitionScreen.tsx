import React, { useState, useEffect, useRef } from 'react';
import {
  StyleSheet,
  View,
  Text,
  Animated,
  Vibration,
  Platform,
} from 'react-native';
import { Camera, useCameraDevice } from 'react-native-vision-camera';
import { useIsFocused } from '@react-navigation/native';
import { useFaceRecognition } from '../hooks/useFaceRecognition';
import { AccessResult } from '../components/UI/AccessResult';
import { StatusIndicator } from '../components/UI/StatusIndicator';
import { detectFaceInImage } from '../services/faceDetection';

export default function FaceRecognitionScreen() {
  const device = useCameraDevice('front');
  const cameraRef = useRef<Camera>(null);
  const isFocused = useIsFocused();
  const { recognize, processing, result, reset } = useFaceRecognition();

  const [systemActive, setSystemActive] = useState(true);
  const [faceDetected, setFaceDetected] = useState(false);
  const [hasPermission, setHasPermission] = useState(false);

  const pulseAnim = useRef(new Animated.Value(1)).current;

  // Solicita permissão de câmera
  useEffect(() => {
    (async () => {
      const status = await Camera.requestCameraPermission();
      setHasPermission(status === 'granted');
    })();
  }, []);

  // Animação de pulso para o círculo de detecção
  useEffect(() => {
    const pulse = Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, {
          toValue: 1.1,
          duration: 1000,
          useNativeDriver: true,
        }),
        Animated.timing(pulseAnim, {
          toValue: 1,
          duration: 1000,
          useNativeDriver: true,
        }),
      ])
    );
    pulse.start();
    return () => pulse.stop();
  }, []);

  // Simula detecção de face (pode ser melhorado com ML Kit em tempo real)
  useEffect(() => {
    if (!processing && !result && systemActive && isActive) {
      // Por enquanto, detecta face após 2 segundos
      // Em produção, use ML Kit para detecção em tempo real
      const timeout = setTimeout(() => {
        setFaceDetected(true);
      }, 2000);

      return () => clearTimeout(timeout);
    }
  }, [processing, result, systemActive, isActive]);

  // Captura e processa foto quando face é detectada
  useEffect(() => {
    let timeout: NodeJS.Timeout;

    if (faceDetected && !processing && !result && systemActive) {
      // Aguarda 1 segundo com face estável antes de capturar
      timeout = setTimeout(() => {
        captureAndRecognize();
      }, 1000);
    }

    return () => clearTimeout(timeout);
  }, [faceDetected, processing, result, systemActive]);

  const captureAndRecognize = async () => {
    if (!cameraRef.current || processing) return;

    try {
      const photo = await cameraRef.current.takePhoto({
        qualityPrioritization: 'quality',
        flash: 'off',
      });

      const imagePath = `file://${photo.path}`;

      // Verifica se há face na imagem
      const faceCheck = await detectFaceInImage(imagePath);
      
      if (!faceCheck.hasFace) {
        setFaceDetected(false);
        return;
      }

      // Envia para API
      const recognitionResult = await recognize(imagePath);

      // Vibra baseado no resultado
      if (recognitionResult.access_granted) {
        Vibration.vibrate([0, 200, 100, 200]); // Sucesso
      } else {
        Vibration.vibrate(500); // Erro
      }

      setFaceDetected(false);
    } catch (error) {
      console.error('Recognition error:', error);
      setFaceDetected(false);
    }
  };

  // Obtém saudação baseada na hora
  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour >= 5 && hour < 12) return 'Bom dia';
    if (hour >= 12 && hour < 18) return 'Boa tarde';
    return 'Boa noite';
  };

  // Formata data
  const formatDate = () => {
    const now = new Date();
    return now.toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
    });
  };

  if (!device || !hasPermission) {
    return (
      <View style={styles.container}>
        <Text style={styles.errorText}>
          {!hasPermission ? 'Permissão de câmera necessária' : 'Câmera não disponível'}
        </Text>
      </View>
    );
  }

  const isActive = systemActive && isFocused && !result;

  return (
    <View style={styles.container}>
      {/* Câmera */}
      <Camera
        ref={cameraRef}
        style={StyleSheet.absoluteFill}
        device={device}
        isActive={isActive}
        photo={true}
        onError={(error) => console.error('Camera error:', error)}
      />

      {/* Overlay */}
      <View style={styles.overlay}>
        {/* Indicador de sistema ativo */}
        <StatusIndicator active={systemActive} text="Sistema ativo" />

        {/* Círculo de detecção central */}
        <View style={styles.centerContainer}>
          <Animated.View
            style={[
              styles.detectionCircle,
              {
                borderColor: faceDetected ? '#10b981' : '#6366f1',
                transform: [{ scale: faceDetected ? 1 : pulseAnim }],
              },
            ]}
          >
            {/* Overlay da câmera na área circular */}
            <View style={styles.cameraCircle} />
          </Animated.View>

          {/* Indicador de rosto detectado */}
          {faceDetected && (
            <View style={styles.faceDetectedBadge}>
              <Text style={styles.faceDetectedText}>✓ Rosto detectado</Text>
            </View>
          )}

          {/* Indicador de processamento */}
          {processing && (
            <View style={styles.processingBadge}>
              <Text style={styles.processingText}>Processando...</Text>
            </View>
          )}
        </View>

        {/* Resultado do reconhecimento */}
        {result && (
          <AccessResult
            granted={result.access_granted}
            employeeName={result.employee?.name}
            message={result.message}
            greeting={getGreeting()}
          />
        )}

        {/* Informações na parte inferior */}
        <View style={styles.bottomInfo}>
          <Text style={styles.timeText}>
            {new Date().toLocaleTimeString('pt-BR', {
              hour: '2-digit',
              minute: '2-digit',
            })}
          </Text>
          <Text style={styles.dateText}>{formatDate()}</Text>
        </View>

        {/* Rodapé */}
        <View style={styles.footer}>
          <Text style={styles.footerText}>
            © 2025 HDT Energy | Sistema de Reconhecimento Facial
          </Text>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
  },
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.3)',
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  detectionCircle: {
    width: 300,
    height: 300,
    borderRadius: 150,
    borderWidth: 4,
    justifyContent: 'center',
    alignItems: 'center',
    overflow: 'hidden',
  },
  cameraCircle: {
    width: '100%',
    height: '100%',
    borderRadius: 150,
  },
  faceDetectedBadge: {
    position: 'absolute',
    bottom: -40,
    backgroundColor: 'rgba(16, 185, 129, 0.9)',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
  },
  faceDetectedText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
  },
  processingBadge: {
    position: 'absolute',
    top: -40,
    backgroundColor: 'rgba(99, 102, 241, 0.9)',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
  },
  processingText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
  },
  bottomInfo: {
    position: 'absolute',
    bottom: 100,
    alignSelf: 'center',
    alignItems: 'center',
  },
  timeText: {
    color: '#fff',
    fontSize: 48,
    fontWeight: 'bold',
    letterSpacing: 2,
  },
  dateText: {
    color: '#9ca3af',
    fontSize: 16,
    marginTop: 4,
  },
  footer: {
    position: 'absolute',
    bottom: 20,
    alignSelf: 'center',
  },
  footerText: {
    color: '#6b7280',
    fontSize: 12,
  },
  errorText: {
    color: '#fff',
    fontSize: 16,
    textAlign: 'center',
    marginTop: '50%',
  },
});

