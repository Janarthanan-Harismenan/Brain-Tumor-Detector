import { useState } from "react";
import { login } from "../api/api";
import { useNavigate } from "react-router-dom";

function Login({ setToken }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate(); // Hook to navigate

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = await login(email, password);
      setToken(data.access_token);  // Store the JWT token
      alert("Logged in successfully!");
      navigate("/prediction");  // Redirect to home page after successful login
    } catch (error) {
      alert("Error during login");
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
        />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default Login;
