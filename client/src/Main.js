import React from "react";

const LOGIN_URI =
  process.env.NODE_ENV !== "production"
    ? "http://localhost:8888/login"
    : "https://spotify-api-profile-app.herokuapp.com/login";

export default function Main() {
  return (
    <>
      <a className="login" href={LOGIN_URI}>
        Login
      </a>
    </>
  );
}
