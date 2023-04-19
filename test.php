<?php
/**
 * Simple example of extending the SQLite3 class and changing the __construct
 * parameters, then using the open method to initialize the DB.
 */
class MyDB extends SQLite3
{
    function __construct()
    {
        $this->open('db.sqlite3');
    }
}

$db = new MyDB();

$res_course = $db->query("SELECT * FROM catalog_course");
$courses = array();

while ($row = $res_course->fetchArray()){
    $course = array($row['title'], $row['description']);
    array_push($courses,$course);
    }

$res_chapter = $db->query("SELECT * FROM catalog_chapter");
$chapters = array();

while ($row = $res_chapter->fetchArray()){
    $chapter = array($row['title'], $row['description']);
    array_push($chapters,$chapter);
    }

$res_questions = $db->query("SELECT * FROM catalog_question");
$questions = array();

while ($row = $res_questions->fetchArray()){
    $question = array($row['title'], $row['question'], $row['answer_points']);
    $res_links = $db->query("SELECT chapter_id FROM catalog_question_chapters WHERE question_id=".$row['id']);
    $rowADD = $res_links->fetchArray();
    array_push($question,$rowADD['chapter_id']);
    array_push($questions,$question);
    }
?>

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Système de messagerie</title>
    <script src="chatinterf.js"></script>
    <link rel="stylesheet" href="test3.css">
</head>
<body>
    <div id="menu">
        <h2>Conversations</h2>
        <ul id="conversations">
            <li data-conversation-id="conversation1">Conversation 1</li>
            <li data-conversation-id="conversation2">Conversation 2</li>
            <li data-conversation-id="conversation3">Conversation 3</li>
        </ul>
        <button id="add-conversation-button">Ajouter une conversation</button>
    <div id="menu">
        <h2>Chapters</h2>
        <?php
        echo '<ul id="conversations">';
        foreach($chapters as $chapter) {
            echo '<li">' . $chapter[0] . '</li>';
        };
        echo '</ul>
              <button id="add-conversation-button">Ajouter
              une conversation</button>';
        ?>
    </div>
    <div id="messages">
        <!-- Les messages de la conversation seront affichés ici -->
    </div>

    <form id="message-form">
        <input type="text" id="message-input" placeholder="Tapez votre message ici" required>
        <button type="submit">Envoyer</button>
    </form>

</body>