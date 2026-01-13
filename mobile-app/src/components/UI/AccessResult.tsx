import React, { useEffect, useRef } from 'react';
import { StyleSheet, View, Text, Animated } from 'react-native';

interface AccessResultProps {
  granted: boolean;
  employeeName?: string;
  message: string;
  greeting: string;
}

export function AccessResult({ granted, employeeName, message, greeting }: AccessResultProps) {
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const scaleAnim = useRef(new Animated.Value(0.8)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 300,
        useNativeDriver: true,
      }),
      Animated.spring(scaleAnim, {
        toValue: 1,
        friction: 8,
        tension: 40,
        useNativeDriver: true,
      }),
    ]).start();
  }, []);

  return (
    <Animated.View
      style={[
        styles.container,
        granted ? styles.success : styles.denied,
        {
          opacity: fadeAnim,
          transform: [{ scale: scaleAnim }],
        },
      ]}
    >
      <View style={styles.iconContainer}>
        <Text style={styles.icon}>{granted ? '✓' : '✗'}</Text>
      </View>

      <Text style={styles.statusText}>
        {granted ? '✓ Acesso Permitido' : '✗ Acesso Negado'}
      </Text>

      {granted && employeeName && (
        <Text style={styles.greetingText}>
          {greeting}, {employeeName}!
        </Text>
      )}

      {!granted && (
        <Text style={styles.messageText}>{message}</Text>
      )}
    </Animated.View>
  );
}

const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    top: '35%',
    alignSelf: 'center',
    padding: 24,
    borderRadius: 20,
    minWidth: 300,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 8,
  },
  success: {
    backgroundColor: 'rgba(16, 185, 129, 0.95)',
  },
  denied: {
    backgroundColor: 'rgba(239, 68, 68, 0.95)',
  },
  iconContainer: {
    width: 64,
    height: 64,
    borderRadius: 32,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
  },
  icon: {
    fontSize: 36,
    color: '#fff',
    fontWeight: 'bold',
  },
  statusText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 8,
  },
  greetingText: {
    color: '#fff',
    fontSize: 28,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  messageText: {
    color: '#fff',
    fontSize: 16,
    textAlign: 'center',
    marginTop: 8,
  },
});
