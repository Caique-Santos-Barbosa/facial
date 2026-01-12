import React from 'react';
import { StyleSheet, View, Text, Animated } from 'react-native';

interface AccessResultProps {
  granted: boolean;
  employeeName?: string;
  message: string;
  greeting: string;
}

export function AccessResult({ granted, employeeName, message, greeting }: AccessResultProps) {
  const fadeAnim = React.useRef(new Animated.Value(0)).current;

  React.useEffect(() => {
    Animated.timing(fadeAnim, {
      toValue: 1,
      duration: 500,
      useNativeDriver: true,
    }).start();
  }, []);

  return (
    <Animated.View
      style={[
        styles.container,
        { opacity: fadeAnim },
        granted ? styles.success : styles.denied,
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
    top: '40%',
    alignSelf: 'center',
    padding: 24,
    borderRadius: 16,
    minWidth: 300,
    alignItems: 'center',
  },
  success: {
    backgroundColor: 'rgba(16, 185, 129, 0.95)',
  },
  denied: {
    backgroundColor: 'rgba(239, 68, 68, 0.95)',
  },
  iconContainer: {
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
  },
  icon: {
    fontSize: 32,
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
    fontSize: 24,
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

