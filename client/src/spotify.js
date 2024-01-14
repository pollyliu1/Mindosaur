import axios from "axios";

// Local storage keys
const LOCALSTORAGE_KEYS = {
  accessToken: "spotify_access_token",
  refreshToken: "spotify_refresh_token",
  expireTime: "spotify_token_expire_time",
  timestamp: "spotify_token_timestamp",
};

// Local storage values
const LOCALSTORAGE_VALUES = {
  accessToken: window.localStorage.getItem(LOCALSTORAGE_KEYS.accessToken),
  refreshToken: window.localStorage.getItem(LOCALSTORAGE_KEYS.refreshToken),
  expireTime: window.localStorage.getItem(LOCALSTORAGE_KEYS.expireTime),
  timestamp: window.localStorage.getItem(LOCALSTORAGE_KEYS.timestamp),
};

/**
 * Checks if the amount of time that has elapsed between the timestamp in localStorage
 * and now is greater than the expiration time which is 3600 sec (1 hour)
 * @returns {boolean} Wheter or not the access token in localStorage has expired
 */
const hasTokenExpired = () => {
  const { accessToken, timestamp, expireTime } = LOCALSTORAGE_VALUES;
  if (!accessToken || !timestamp) {
    return false;
  }
  const millisecondsElapsed = Date.now() - Number(timestamp); // Get the elapsed time by subtracting the current timestamp to the timestamp that the accessToken has been created on the localStorage.
  return millisecondsElapsed / 1000 > Number(expireTime); // Convert the elapse milisec to sec and compare to the expireTime (3600 sec)
};

/**
 * Clear out all localStorage items and reload page
 * @returns {void}
 */
export const logout = () => {
  for (const property in LOCALSTORAGE_KEYS) {
    window.localStorage.removeItem(LOCALSTORAGE_KEYS[property]);
  }
  // Navigate to homepage
  window.location = window.location.origin;
};

/**
 * Use the refresh token stored in localStorage and hit the /refresh_token route in node app, then update values in localStorage
 * using the data from the response
 * @returns {void}
 */
const refreshToken = async () => {
  try {
    // Logout if there's no refresh token stored or we've managed to get into a reload infinite loop
    if (
      !LOCALSTORAGE_KEYS.refreshToken ||
      LOCALSTORAGE_VALUES.refreshToken === "undefined" ||
      Date.now() - Number(LOCALSTORAGE_VALUES.timestamp) / 1000 < 1000
    ) {
      console.error("No refresh token available");
      logout();
    }

    // Go to 'refresh_token' endpoint or route in our node app where we can get a response of "data" which contains new values
    //  of access and refresh_token, token_type, token_expiry in 3600 seconds, and the scope
    const { data } = await axios.get(
      `/refresh_token?refresh_token=${LOCALSTORAGE_VALUES.refreshToken}`
    );

    // update the localStorage using the response data from refresh_token endpoint
    window.localStorage.setItem(
      LOCALSTORAGE_KEYS.accessToken,
      data.access_token
    );
    window.localStorage.setItem(LOCALSTORAGE_KEYS.timestamp, Date.now());

    // reload the page for localStorage updates to be reflected
    window.location.reload();
  } catch (e) {
    console.error(e);
  }
};

const getAccessToken = () => {
  const queryString = window.location.search; // returns the url after "?"
  const urlParams = new URLSearchParams(queryString); // converts the url to an object
  const queryParams = {
    [LOCALSTORAGE_KEYS.accessToken]: urlParams.get("access_token"),
    [LOCALSTORAGE_KEYS.refreshToken]: urlParams.get("refresh_token"),
    [LOCALSTORAGE_KEYS.expireTime]: urlParams.get("expires_in"),
  };

  const hasError = urlParams.get("error");

  if (queryParams[LOCALSTORAGE_KEYS.accessToken]) {
    // If there is a token in the URL query params, then first log in
    // Store the query params in localStorage
    for (const property in queryParams) {
      window.localStorage.setItem(property, queryParams[property]);
    }
    // Set timestamp
    window.localStorage.setItem(LOCALSTORAGE_KEYS.timestamp, Date.now());
    // Return access token from query params
    return queryParams[LOCALSTORAGE_KEYS.accessToken];
  }

  // If there is an error or access token has expired or there is no access token, then refresh the token
  if (
    hasError ||
    hasTokenExpired() ||
    window.localStorage.getItem(LOCALSTORAGE_KEYS.accessToken) === "undefined"
  ) {
    refreshToken();
  }

  if (
    LOCALSTORAGE_KEYS.accessToken &&
    LOCALSTORAGE_KEYS.accessToken !== "undefined"
  ) {
    // If there is a valid access token in local storage, use that
    return LOCALSTORAGE_VALUES.accessToken;
  }

  return false;
};

export const accessToken = getAccessToken();

/**
 * Axios global req headers
 * https://axios-http.com/docs/config_defaults
 */

axios.defaults.baseURL = "https://api.spotify.com/v1/";
axios.defaults.headers["Authorization"] = `Bearer ${accessToken}`;
axios.defaults.headers["Content-type"] = "application/json";
axios.defaults.headers["Accept"] = "application/json";

/**
 * Get current users profile
 * https://developer.spotify.com/console/get-current-user/
 * @returns {Promise}
 */

export const getCurrentUserProfile = () => axios.get("/me"); // Global axios baseURL

/**
 * Return current users playlists
 * https://developer.spotify.com/documentation/web-api/reference/#/operations/get-a-list-of-current-users-playlists
 * @returns {Promise}
 */
export const getCurrentUserPlaylists = (limit = 20) => {
  return axios.get(`/me/playlists?limit=${limit}`);
};

/**
 * Return current users top artists
 * https://developer.spotify.com/documentation/web-api/reference/#/operations/get-users-top-artists-and-tracks
 * @param {string} time_range
 * @returns {Promise}
 */
export const getUserTopArtists = (time_range) => {
  return axios.get(`/me/top/artists?time_range=${time_range}`);
};

/**
 * Return current users top tracks
 * https://developer.spotify.com/documentation/web-api/reference/#/operations/get-users-top-artists-and-tracks
 * @param {string} time_range
 * @returns {Promise}
 */
export const getUserTopTracks = (time_range) => {
  return axios.get(`/me/top/tracks?time_range=${time_range}`);
};

/**
 * Return artist details
 * https://developer.spotify.com/documentation/web-api/reference/#/operations/get-an-artist
 * @param {string} artistId
 * @returns {Promise}
 */
export const getArtistById = (artistId) => {
  return axios.get(`/artists/${artistId}`);
};

// To figure out https://developer.spotify.com/console/artists/
// export const getArtistTracksById = (artistId) => {
//     return axios.get(`artists/${artistId}/top-tracks`)
// }

export const getRelatedArtists = (artistId) => {
  return axios.get(`/artists/${artistId}/related-artists`);
};

export const getArtistAlbums = (artistId) => {
  return axios.get(`/artists/${artistId}/albums`);
};

export const getPlaylistById = (playlistId) => {
  return axios.get(`/playlists/${playlistId}`);
};

/**
 * Return tracks
 * https://developer.spotify.com/console/tracks/
 * @param {string} trackId
 * @returns {Promise}
 */
export const getTrackById = (trackId) => {
  return axios.get(`/tracks/${trackId}`);
};

export const getTrackFeatures = (trackId) => {
  return axios.get(`/audio-features/${trackId}`);
};

/**
 * Return album and single tracks and details
 * https://developer.spotify.com/documentation/web-api/reference/#/operations/get-an-albums-tracks
 * @param {string} albumId
 * @returns {Promise}
 */

export const getAlbumById = (albumId) => {
  return axios.get(`/albums/${albumId}`);
};

export const getAlbumTracksById = (albumId) => {
  return axios.get(`/albums/${albumId}/tracks`);
};
