import PropTypes from "prop-types";
import React, { useState, useEffect, useRef } from 'react';
import "./style.css";

import PickCard from "../../components/swipe-deck/pick-card/pick-card";
import AuthForm from "../../components/auth-form";
import { getAuth, onAuthStateChanged } from "firebase/auth";

interface Props {
} // Empty

interface Movie {
    ID: string;
    Name: string;
    Poster: string;
    [key: string]: any; // Allow other properties
}

export const Main = ({}: Props): JSX.Element => {
    const [movies, setMovies] = useState<Movie[]>([]);
    const [user, setUser] = useState<any>();
    const auth = getAuth();

    onAuthStateChanged(auth, (changedUser) => {
        // TODO Why does this get called so many times?
        if (changedUser) {
            setUser(changedUser)
        } else {
            setUser(NaN)
        }
    });

    useEffect(() => {
        if (user && user.uid) {
            fetchMovies(user.uid);
        }
    }, [user?.uid]);

    useEffect(() => {
        console.log("Main screen mounted");
    }, []);

    const fetchMovies = async (uid: string) => {
        fetch(`http://localhost:5000/users/` + encodeURIComponent(uid) + `/movies`)
            .then((response) => response.json())
            .then((data) => {
                data = data.movies
                setMovies(data)
            });
    };
    
    return (
        <div className="flex justify-center items-center min-h-screen"> 
            {user
                ? <PickCard
                    uid={user.uid}
                    cardList={movies}
                    onEvaluate={(card) => {
                        setMovies((prev) => prev.filter((c) => c.Name !== card.Name));            
                    }}
                />
                : <AuthForm /> 
            }
        </div>
    );
};