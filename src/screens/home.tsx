
import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { RootStackParamList } from '../navigation/appnav';

type Props = NativeStackScreenProps<RootStackParamList, 'Home'>;

export default function HomeScreen({ navigation }: Props) {
  return (
    <View style={styles.container}>
      {/* Main content */}
      <View style={styles.main}>
        <Text style={styles.title}>Welcome to the Home Screen!</Text>
        <Text style={styles.subtitle}>Choose an action below.</Text>
      </View>

      {/* Bottom bar */}
      <View style={styles.bottomBar}>
        <Button
          title="Create Profile"
          color = '#9F4CFC'
          onPress={() => navigation.navigate('CreateProfile')}
        />
        <Button
          title="View Profile"
          color = '#9F4CFC'
          onPress={() => navigation.navigate('ViewProfile')}
        />
        <Button
          title="Create Post"
          color = '#62139E'
          onPress={() => navigation.navigate('CreatePost')}
        />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  main: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  title: { fontSize: 24, fontWeight: '600', marginBottom: 8 },
  subtitle: { fontSize: 16, color: '#7F00DE' },

  bottomBar: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    paddingVertical: 12,
    borderTopWidth: 1,
    borderColor: '#ccc',
    backgroundColor: '#f9f9f9',
  },
});
