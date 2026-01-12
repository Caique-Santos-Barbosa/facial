import React from 'react';
import { StyleSheet, View, Text } from 'react-native';

interface StatusIndicatorProps {
  active: boolean;
  text: string;
}

export function StatusIndicator({ active, text }: StatusIndicatorProps) {
  return (
    <View style={styles.container}>
      <View style={[styles.dot, active && styles.dotActive]} />
      <Text style={styles.text}>{text}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    top: 50,
    left: 20,
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
  },
  dot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: '#ef4444',
    marginRight: 8,
  },
  dotActive: {
    backgroundColor: '#10b981',
  },
  text: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '500',
  },
});

