package worker;

import redis.clients.jedis.Jedis;
import redis.clients.jedis.exceptions.JedisConnectionException;
import java.sql.*;
import org.json.JSONObject;

class Worker {
  public static void main(String[] args) {
    try {
      Jedis redis = connectToRedis("redis");
      Connection dbConn = connectToDB("db");

      System.err.println("Watching vote queue");

      while (true) {
        String voteJSON = redis.blpop(0, "votes").get(1);
        JSONObject voteData = new JSONObject(voteJSON);
        String voterID = voteData.getString("voter_id");
        
        //A
        String voteA = voteData.getString("voteA");
        if (!voteA.equals("")) {
          String category = "A";
          System.err.printf("Processing vote for '%s' in category '%s' by '%s'\n", voteA, category, voterID);
          updateVote(dbConn, voterID, voteA, category);
        }

        //B
        String voteB = voteData.getString("voteB");
        if (!voteB.equals("")) {
          String category = "B";
          System.err.printf("Processing vote for '%s' in category '%s' by '%s'\n", voteB, category, voterID);
          updateVote(dbConn, voterID, voteB, category);
        }

        //C
        String voteC = voteData.getString("voteC");
        if (!voteC.equals("")) {
          String category = "C";
          System.err.printf("Processing vote for '%s' in category '%s' by '%s'\n", voteC, category, voterID);
          updateVote(dbConn, voterID, voteC, category);
        }

        //D
        String voteD = voteData.getString("voteD");
        if (!voteD.equals("")) {
          String category = "D";
          System.err.printf("Processing vote for '%s' in category '%s' by '%s'\n", voteD, category, voterID);
          updateVote(dbConn, voterID, voteD, category);
        }
        
        //E
        String voteE = voteData.getString("voteE");
        if (!voteE.equals("")) {
          String category = "E";
          System.err.printf("Processing vote for '%s' in category '%s' by '%s'\n", voteE, category, voterID);
          updateVote(dbConn, voterID, voteE, category);
        }

        //F
        String voteF = voteData.getString("voteF");
        if (!voteF.equals("")) {
          String category = "F";
          System.err.printf("Processing vote for '%s' in category '%s' by '%s'\n", voteF, category, voterID);
          updateVote(dbConn, voterID, voteF, category);
        }
      }
    } catch (SQLException e) {
      e.printStackTrace();
      System.exit(1);
    }
  }

  static void updateVote(Connection dbConn, String voterID, String vote, String category) throws SQLException {
    PreparedStatement insert = dbConn.prepareStatement(
      "INSERT INTO votes (id, vote, cat) VALUES (?, ?, ?)");
    insert.setString(1, voterID);
    insert.setString(2, vote);
    insert.setString(3, category);

    try {
      insert.executeUpdate();
      System.err.printf("INSERTED vote for '%s' in category '%s' by '%s'\n", vote, category, voterID);
    } catch (SQLException e) {
      PreparedStatement update = dbConn.prepareStatement(
        "UPDATE votes SET vote = ? WHERE id = ? AND cat = ?");
      update.setString(1, vote);
      update.setString(2, voterID);
      update.setString(3, category);
      update.executeUpdate();
      System.err.printf("UPDATED vote for '%s' in category '%s' by '%s'\n", vote, category, voterID);
    }
  }

  static Jedis connectToRedis(String host) {
    Jedis conn = new Jedis(host);

    while (true) {
      try {
        conn.keys("*");
        break;
      } catch (JedisConnectionException e) {
        System.err.println("Waiting for redis");
        sleep(1000);
      }
    }

    System.err.println("Connected to redis");
    return conn;
  }

  static Connection connectToDB(String host) throws SQLException {
    Connection conn = null;

    try {

      Class.forName("org.postgresql.Driver");
      String url = "jdbc:postgresql://" + host + "/postgres";

      while (conn == null) {
        try {
          conn = DriverManager.getConnection(url, "postgres", "postgres");
        } catch (SQLException e) {
          System.err.println("Waiting for db from Java worker!!");
          sleep(1000);
        }
      }

      PreparedStatement st1 = conn.prepareStatement(
        "DROP TABLE IF EXISTS votes");
      st1.executeUpdate();
      PreparedStatement st = conn.prepareStatement(
        "CREATE TABLE IF NOT EXISTS votes (id VARCHAR(255) NOT NULL, vote VARCHAR(255) NOT NULL, cat VARCHAR(255) NOT NULL UNIQUE)");
      st.executeUpdate();

    } catch (ClassNotFoundException e) {
      e.printStackTrace();
      System.exit(1);
    }

    System.err.println("Connected to db from Java worker!!");
    return conn;
  }

  static void sleep(long duration) {
    try {
      Thread.sleep(duration);
    } catch (InterruptedException e) {
      System.exit(1);
    }
  }
}
