

import React, { useState } from 'react';
import { View, TextInput, Button, StyleSheet } from 'react-native';

export default function CreatePostScreen() {
  const [text, setText] = useState('');

  return (
    <View style={styles.container}>
      <TextInput
        style={styles.box}
        placeholder="Write your post..."
        value={text}
        onChangeText={setText}
        multiline
      />

      <Button 
        title="Save"  
        color = '#6624A3' 
        onPress={() => console.log('Post saved:', text)} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { padding: 20, flex: 1 },
  box: {
    borderWidth: 1,
    borderColor: '#ccc',
    padding: 15,
    borderRadius: 10,
    height: 200,
  },
});
