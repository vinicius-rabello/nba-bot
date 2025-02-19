DROP TABLE IF EXISTS games;
CREATE TABLE games (
	game_id VARCHAR(10) PRIMARY KEY,
	date DATE NOT NULL,
	time VARCHAR(50),
	broadcaster VARCHAR(50),
	home_team VARCHAR(50) NOT NULL,
	away_team VARCHAR(50) NOT NULL,
	home_team_score INTEGER CHECK (home_team_score >= 0 OR home_team_score IS NULL),
	away_team_score INTEGER CHECK (away_team_score >= 0 OR away_team_score IS NULL),
	arena VARCHAR(50),
	city VARCHAR(50),
	state VARCHAR(2) CHECK (LENGTH(state) = 2)
);
