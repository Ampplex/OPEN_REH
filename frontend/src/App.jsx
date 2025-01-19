import React from 'react'
import Interface from './components/Interface'
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Output from './components/Output';

const App = () => {
  return (
    <div className='w-full h-screen'>
    
      <Routes>
          <Route path='/' index element={<Interface />} />
          <Route path='/output' element={<Output />} />
      </Routes>
  
    </div>
  )
}

export default App