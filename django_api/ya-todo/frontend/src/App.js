import React, { Component } from 'react';
import axios from 'axios';

const BACKEND_URL = 'http://localhost:8000/api/';

class App extends Component {
  state = {
    todos: []
  };

  componentDidMount() {
    this.getTodos();
  }

  getTodos() {
    axios.get(BACKEND_URL).
      then(res => {
        this.setState({ todos: res.data });
      })
      .catch(err => {
        console.log(err);
      });
  }

  render() {
    return (
        <div>
          {this.state.todos.map(item => (
           <div key={item.id}>
             <h1>{item.id} - {item.title}</h1>

             <span>{item.body}</span>
           </div>
         ))}
      </div>
    )
  }
}

export default App;
