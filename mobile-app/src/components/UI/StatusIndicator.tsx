import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

interface StatusIndicatorProps {
  active: boolean;
  text: string;
}

export function StatusIndicator({ active, text }: StatusIndicatorProps) {
  return (
    <View style={styles.container}>
      <View style={[styles.dot, active && styles.activeDot]} />
      <Text style={styles.text}>{text}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    top: 60,
    right: 20,
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(0, 0, 0, 0.6)',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 20,
  },
  dot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: '#6b7280',
    marginRight: 8,
  },
  activeDot: {
    backgroundColor: '#10b981',
  },
  text: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '500',
  },
});
