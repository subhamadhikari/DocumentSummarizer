import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import Login from './pages/Login.jsx'
import './index.css'
import {Provider} from "react-redux"
import {store} from "./redux/store.js"
import {BrowserRouter,Routes,Route} from "react-router-dom"


ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Provider store={store}>
      <BrowserRouter>
        <Routes>
          <Route path='/' element={<App/>}/>
          <Route path='/login' element={<Login/>}/>
        </Routes>
      </BrowserRouter>
      {/* <App /> */}
      {/* <Login/> */}
    </Provider>
  </React.StrictMode>,
)
