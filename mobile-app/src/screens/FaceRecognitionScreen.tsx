import React, { useState, useEffect, useRef } from 'react';
import { StyleSheet, View, Text, Animated, Vibration, StatusBar } from 'react-native';
import { Camera, useCameraDevice } from 'react-native-vision-camera';
import { recognizeFace } from '../services/api';
import { AccessResult } from '../components/UI/AccessResult';
import { StatusIndicator } from '../components/UI/StatusIndicator';

export default function FaceRecognitionScreen() {
  const device = useCameraDevice('front');
  const cameraRef = useRef<Camera>(null);

  const [hasPermission, setHasPermission] = useState(false);
  const [systemActive, setSystemActive] = useState(true);
  const [recognitionResult, setRecognitionResult] = useState<any>(null);
  const [processing, setProcessing] = useState(false);

  const pulseAnim = useRef(new Animated.Value(1)).current;

  // Request camera permission
  useEffect(() => {
    (async () => {
      const status = await Camera.requestCameraPermission();
      setHasPermission(status === 'granted');
    })();
  }, []);

  // Pulse animation
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

  // Auto capture every 3 seconds
  useEffect(() => {
    if (!systemActive || recognitionResult || processing) return;

    const interval = setInterval(() => {
      captureAndRecognize();
    }, 3000);

    return () => clearInterval(interval);
  }, [systemActive, recognitionResult, processing]);

  const captureAndRecognize = async () => {
    if (!cameraRef.current || processing || recognitionResult) return;

    setProcessing(true);

    try {
      const photo = await cameraRef.current.takePhoto({
        qualityPrioritization: 'quality',
        flash: 'off',
      });

      const formData = new FormData();
      formData.append('image', {
        uri: `file://${photo.path}`,
        type: 'image/jpeg',
        name: 'face.jpg',
      } as any);

      const result = await recognizeFace(formData);

      // Vibration feedback
      if (result.access_granted) {
        Vibration.vibrate([0, 200, 100, 200]); // Success pattern
      } else {
        Vibration.vibrate(500); // Error
      }

      setRecognitionResult(result);

      // Reset after 5 seconds
      setTimeout(() => {
        setRecognitionResult(null);
        setProcessing(false);
      }, 5000);

    } catch (error) {
      console.error('Recognition error:', error);
      setProcessing(false);
    }
  };

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour >= 5 && hour < 12) return 'Bom dia';
    if (hour >= 12 && hour < 18) return 'Boa tarde';
    return 'Boa noite';
  };

  const formatDate = () => {
    return new Date().toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
    });
  };

  const formatTime = () => {
    return new Date().toLocaleTimeString('pt-BR', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (!hasPermission) {
    return (
      <View style={styles.container}>
        <Text style={styles.errorText}>Permissão de câmera negada</Text>
      </View>
    );
  }

  if (!device) {
    return (
      <View style={styles.container}>
        <Text style={styles.errorText}>Câmera não disponível</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" />
      
      {/* Camera */}
      <Camera
        ref={cameraRef}
        style={StyleSheet.absoluteFill}
        device={device}
        isActive={systemActive && !recognitionResult}
        photo={true}
      />

      {/* Overlay */}
      <View style={styles.overlay}>
        {/* Status Indicator */}
        <StatusIndicator active={systemActive} text="Sistema ativo" />

        {/* Center Detection Circle */}
        <View style={styles.centerContainer}>
          <Animated.View
            style={[
              styles.detectionCircle,
              {
                borderColor: processing ? '#10b981' : '#6366f1',
                transform: [{ scale: processing ? 1 : pulseAnim }],
              },
            ]}
          >
            {processing && (
              <View style={styles.faceDetectedBadge}>
                <Text style={styles.badgeText}>✓ Rosto detectado</Text>
              </View>
            )}
          </Animated.View>
        </View>

        {/* Recognition Result */}
        {recognitionResult && (
          <AccessResult
            granted={recognitionResult.access_granted}
            employeeName={recognitionResult.employee?.name}
            message={recognitionResult.message}
            greeting={getGreeting()}
          />
        )}

        {/* Bottom Info */}
        <View style={styles.bottomInfo}>
          <Text style={styles.timeText}>{formatTime()}</Text>
          <Text style={styles.dateText}>{formatDate()}</Text>
        </View>

        {/* Footer */}
        <View style={styles.footer}>
          <Text style={styles.footerText}>
            © 2026 HDT Energy | Sistema de Reconhecimento Facial
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
    justifyContent: 'flex-end',
    alignItems: 'center',
    paddingBottom: 20,
  },
  faceDetectedBadge: {
    backgroundColor: 'rgba(16, 185, 129, 0.9)',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
  },
  badgeText: {
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
  },
});
