import React from "react";

const LogBtn = () => {
  const [loggedIn, setLoggedIn] = React.useState(false);
  return (
    <div className={`${loggedIn ? "bg-red-500" : "bg-green-500"} flex m-3 p-2 rounded-2xl`}>
      {loggedIn ? (
        <button onClick={() => setLoggedIn(false)}>Log Out</button>
      ) : (
        <button onClick={() => setLoggedIn(true)}>Log In</button>
      )}
    </div>
  );
};

export default LogBtn;
