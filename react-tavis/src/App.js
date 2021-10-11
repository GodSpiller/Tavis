import './App.css';
import NavBar from '../src/components/NavBar.js'
import Fridge from '../src/pages/Fridge'
import Recipes from '../src/pages/Recipes'
import Settings from '../src/pages/Settings'

import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";

function App() {
  return (
    <Router>
      <NavBar/>
      <Switch>
        <Route path='/Opskrifter' component={Recipes} />
        <Route path='/Køleskab' component={Fridge} />
        <Route path='/Indstillinger' component={Settings} />
      </Switch>
    </Router>
  );
}

export default App;
