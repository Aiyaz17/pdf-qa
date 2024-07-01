import axios from "axios";
import Chat from "./components/Chat";
import Navbar from "./components/Navbar";
import 'react-toastify/dist/ReactToastify.css';
import { ToastContainer } from 'react-toastify';
import { useState } from "react";

function App() {
  axios.defaults.baseURL = process.env.REACT_APP_BACKEND_URL;
  const [pdf, setPdf] = useState(null);

  return (
    <div className="App">
      <Navbar pdf={pdf} setPdf={setPdf} />
      <Chat pdf={pdf} />
      <ToastContainer />
    </div>
  );
}

export default App;
