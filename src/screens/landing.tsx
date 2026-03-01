
import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { RootStackParamList } from '../navigation/appnav';

type Props = NativeStackScreenProps<RootStackParamList, 'Landing'>;

export default function LandingScreen({ navigation }: Props) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome to TraceNote</Text>

      <View style={styles.buttons}>
        <Button 
            title="Sign Up"
            color = '#7D3ACF' 
            onPress={() => navigation.navigate('Signup')} />
        <Button 
            title="Log In" 
            color = '#7D3ACF'
            onPress={() => navigation.navigate('Login')} />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20 },
  title: { fontSize: 32, fontWeight: '700', marginBottom: 40, textAlign: 'center' },
  buttons: { width: '80%', gap: 20 },
});
