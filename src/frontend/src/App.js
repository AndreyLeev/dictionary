import React from 'react';

import { Switch, Route } from 'react-router-dom';

import DictionaryList from './components/DictionaryList'
import DictionaryDetail from './components/DictionaryDetail'


function App() {
  return (
      <Switch>
          <Route exact path='/' component={DictionaryList}/>
          <Route path='/dictionaries' component={DictionaryList}/>
          <Route path='/dictionary-details/:dictionaryId' component={DictionaryDetail}/>
      </Switch>
  );
}

export default App;
