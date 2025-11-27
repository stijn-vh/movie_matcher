import PropTypes from "prop-types";
import React, { useState, useEffect, useRef } from 'react';
import "./style.css";

import AuthForm from "../../components/auth-form";
import { getAuth, onAuthStateChanged, signOut } from "firebase/auth";
import { GroupList } from "../../components/group-list/group-list";
import { CardList } from "../card_list/main";

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

    const handleLogout = async () => {
        try {
            await signOut(auth);
            setUser(null);
            setScreenState('auth');
            setGroups([]);
            setCurrentGroup(undefined);
        } catch (error) {
            console.error('Failed to log out:', error);
        }
    };

    const createUserProfile = async (user: any): Promise<Response> => {
        try {
            const token = await user.getIdToken();
            const response = await fetch('http://localhost:5000/users/init', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    "Authorization": `Bearer ${token}`,
                },
                body: JSON.stringify({}),
            });
            return response;
        } catch (error) {
            console.error('Failed to create user', error);
            throw error;
        }
    }
    
    useEffect(() => {
        const unsubscribe = onAuthStateChanged(auth, async (changedUser) => {
            if (changedUser == null) { return }
            const token = await changedUser.getIdToken();

            if (changedUser) {
                await fetch('http://localhost:5000/users/get', {
                    headers: {
                        'Authorization': `Bearer ${token}` // Add authorization header
                    }
                })
                .then(async (response) => {
                    if (response.status == 404) {
                        response = await createUserProfile(changedUser)
                    }

                    if (!response.ok) {
                        throw new Error('Authentication failed')
                    }
                    return response.json()
                })
                .then((data) => {
                    setUser(data.user)

                    if (data.user.active_group != null) {
                        onGroupJoined(data.user.active_group)
                    } else {
                        fetchGroups()
                    }
                })
                .catch((e) => {
                    console.log(e)
                    setUser(null);
                    setScreenState('auth');
                })
            }
        });

        return () => unsubscribe();
    }, []); 

    const fetchGroups = async () => {
        fetch(`http://localhost:5000/groups/all`)
            .then((response) => response.json())
            .then((data) => {
                data = data.groups
                setGroups(data)
            });

        setScreenState('groups')
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
                return <CardList user={user} />
        }
    }

return (
    <div className="flex justify-center items-center min-h-screen"> 
        { renderScreen() }
        {user && (
            <button onClick={handleLogout} className="absolute top-4 right-4 px-4 py-2 btn btn-soft btn-secondary">
                Log Out
            </button>
        )}
    </div>
    );
};