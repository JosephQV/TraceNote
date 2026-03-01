
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

export default function ViewProfileScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Your Profile</Text>
      <Text>Username: (placeholder)</Text>
      <Text>Bio: (placeholder)</Text>
      <Text>Pronouns: (placeholder)</Text>
      <Text>Interests: (placeholder)</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { padding: 20, flex: 1 },
  title: { fontSize: 28, fontWeight: '700', marginBottom: 20 },
});