import PropTypes from "prop-types";
import React, { useState, useEffect, useRef } from 'react';
import "./style.css";

import AuthForm from "../../components/auth-form";
import { getAuth, onAuthStateChanged } from "firebase/auth";
import { GroupList } from "../../components/group-list/group-list";

interface Props {
} // Empty

interface Group { // Should move to interface file
    id: string;
    name: string;
}


export const Main = ({}: Props): JSX.Element => {
    const [user, setUser] = useState<any>();
    const [screenState, setScreenState] = useState<string>();
    const [groups, setGroups] = useState<Group[]>([])
    const [group, setCurrentGroup] = useState<Group>();
    const auth = getAuth();

    onAuthStateChanged(auth, (changedUser) => {
        if (changedUser) {
            setUser(changedUser)
        } else {
            setUser(NaN)
            setScreenState('auth')
        }
    });

    useEffect(() => {
        if (user && user.uid) {
            if (user.active_group != '') {
                // Fetch group
            }
            else {
                fetchGroups();
            }
            fetchGroups()
        }
    }, [user?.uid]);

    useEffect(() => {}, []);

    const fetchGroups = async () => {
        fetch(`http://localhost:5000/group/all`)
            .then((response) => response.json())
            .then((data) => {
                data = data.groups
                setGroups(data)
            });
        
        setScreenState('groups')
    };

    const fetchGroupMovies = async () => {
        fetch(`http://localhost:5000/group/${group?.id}/movies/${user.uid}`)
        .then((response) => response.json())
        .then((data) => {
            console.log(data)
        });
    };
    
    const onGroupJoined = (group: Group) => {
        setScreenState('group_movies')
        setCurrentGroup(group)
    };

    const renderScreen = () => {
        switch(screenState) {
            case 'auth':
                return <AuthForm />
            case 'groups':
                return <GroupList uid={user.uid} onGroupJoined={onGroupJoined} />
            case 'group_movies':
                fetchGroupMovies()
                return <p>Joined group {group?.name}!</p>
        }
    }
return (
    <div className="flex justify-center items-center min-h-screen"> 
        { renderScreen() }
    </div>
    );
};