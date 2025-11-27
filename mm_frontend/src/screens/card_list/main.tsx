import PropTypes from "prop-types";
import React, { useState, useEffect, useRef } from 'react';
import "./style.css";

import PickCard from "../../components/swipe-deck/pick-card/pick-card";
import AuthForm from "../../components/auth-form";
import { getAuth } from "firebase/auth";

interface Props {
    user: any; // Create user object
}

interface Movie {
    ID: string;
    Name: string;
    Poster: string;
    [key: string]: any; 
}

export const CardList = ({ user }: Props): JSX.Element => {
    const [movies, setMovies] = useState<Movie[]>([]);

    useEffect(() => {
        if (user && user.uid && user.active_group) {
            fetchMovies(user);
        }
    }, [user?.uid, user?.active_group]);

    const fetchMovies = async (user: any) => {
        const currentUser = getAuth().currentUser;
        if (!currentUser) {
            return;
        }
        const token = await currentUser.getIdToken();

        fetch(`http://localhost:5000/groups/` + encodeURIComponent(user.active_group) + `/movies/`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then((response) => response.json())
        .then((data) => {
            setMovies(data.movies)
        });
    };
    
    return (
        <div className="flex justify-center items-center min-h-screen"> 
            {user
                ? <PickCard
                    user={user}
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