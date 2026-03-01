
import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet } from 'react-native';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { RootStackParamList } from '../navigation/appnav';

type Props = NativeStackScreenProps<RootStackParamList, 'CreateProfile'>;

export default function CreateProfileScreen({ navigation }: Props) {
  const [bio, setBio] = useState('');
  const [pronouns, setPronouns] = useState('');
  const [interests, setInterests] = useState('');

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Create Profile</Text>

      <TextInput
        style={styles.input}
        placeholder="Bio"
        value={bio}
        onChangeText={setBio}
      />
      <TextInput
        style={styles.input}
        placeholder="Pronouns"
        value={pronouns}
        onChangeText={setPronouns}
      />
      <TextInput
        style={styles.input}
        placeholder="Interests"
        value={interests}
        onChangeText={setInterests}
      />

      <Button
        title="Save Profile"
        color = '#6624A3'
        onPress={() => {
          // later: call API, then navigate
          navigation.navigate('Home');
        }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, justifyContent: 'center' },
  title: { fontSize: 28, fontWeight: '700', marginBottom: 20, textAlign: 'center' },
  input: { borderWidth: 1, borderColor: '#ccc', padding: 12, borderRadius: 8, marginBottom: 12 },
});
