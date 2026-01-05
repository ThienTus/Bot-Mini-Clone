import { useEffect, useState } from "react";
import api from "./services/api";

function App() {
  const [status, setStatus] = useState("");

  useEffect(() => {
    api.get("/health")
      .then(res => setStatus(res.data.message))
      .catch(err => console.error(err));
  }, []);

  return (
    <div>
      <h1>React + Node.js</h1>
      <p>{status}</p>
    </div>
  );
}

export default App;
