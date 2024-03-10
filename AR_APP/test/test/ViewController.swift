//
//  ViewController.swift
//  test
//
//  Created by 劉世文 on 2/29/24.
//

import UIKit
import SceneKit
import ARKit
import RealityKit

class ViewController: UIViewController, ARSCNViewDelegate, AVAudioRecorderDelegate, AVAudioPlayerDelegate {
    var tankNode: SCNNode?
    var audioRecorder: AVAudioRecorder?
    var audioPlayer: AVAudioPlayer?
    var isRecording = false
    var record_state = "Record"
    var base_url = "https://511a-140-117-193-176.ngrok-free.app"
    var downloadedAudioURL: URL?
    
    @IBAction func downloadAndPlayAudio(_ sender: UIButton) {
        guard let url = URL(string: base_url + "/download_audio") else { return }
        let sessionConfig = URLSessionConfiguration.default
        let session = URLSession(configuration: sessionConfig)
        
        let downloadTask = session.downloadTask(with: url) { [weak self] tempLocalUrl, response, error in
            if let tempLocalUrl = tempLocalUrl, error == nil {
                // Success
                if let statusCode = (response as? HTTPURLResponse)?.statusCode {
                    print("Successfully downloaded. Status code: \(statusCode)")
                }
                
                do {
                    // Choose the local file URL to save the downloaded file
                    let documentsPath = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
                    let localFileUrl = documentsPath.appendingPathComponent(url.lastPathComponent)
                    
                    // Move the downloaded file from the temporary URL to the desired URL
                    if FileManager.default.fileExists(atPath: localFileUrl.path) {
                        try FileManager.default.removeItem(at: localFileUrl)
                    }
                    try FileManager.default.moveItem(at: tempLocalUrl, to: localFileUrl)
                    
                    // Save the downloaded file URL and play the audio
                    DispatchQueue.main.async {
                        self?.downloadedAudioURL = localFileUrl
                        self?.playDownloadedAudio()
                    }
                } catch (let writeError) {
                    print("Error writing file \(url.lastPathComponent) : \(writeError)")
                }
                
            } else {
                print("Error took place while downloading a file. Error description: \(error?.localizedDescription ?? "")")
            }
        }
        downloadTask.resume()
    }
        
    func playDownloadedAudio() {
        guard let downloadedAudioURL = downloadedAudioURL else { return }
        
        do {
            audioPlayer = try AVAudioPlayer(contentsOf: downloadedAudioURL)
            audioPlayer?.play()
        } catch {
            print("Error playing downloaded audio: \(error.localizedDescription)")
        }
    }
    
    func setupAudioRecorder() {
        let recordingSession = AVAudioSession.sharedInstance()
        do {
            try recordingSession.setCategory(.playAndRecord, mode: .default)
            try recordingSession.setActive(true)
        } catch {
            // Handle session setup failure
        }
        
        let audioFilename = getDocumentsDirectory().appendingPathComponent("recording.m4a")
        
        let settings = [
            AVFormatIDKey: Int(kAudioFormatMPEG4AAC),
            AVSampleRateKey: 12000,
            AVNumberOfChannelsKey: 1,
            AVEncoderAudioQualityKey: AVAudioQuality.high.rawValue
        ]
        
        do {
            audioRecorder = try AVAudioRecorder(url: audioFilename, settings: settings)
            audioRecorder?.delegate = self
            audioRecorder?.prepareToRecord()
        } catch {
            // Handle AVAudioRecorder setup failure
        }
    }
    
    func getDocumentsDirectory() -> URL {
        let paths = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)
        return paths[0]
    }
    
    @IBAction func toggleRecordingPlayback(_ sender: UIButton) {
        switch record_state {
        case "Record":
            do {
                try AVAudioSession.sharedInstance().setActive(true)
                audioRecorder?.record()
                record_state = "Stop"
                print("Record ")
            } catch {
                // Handle recording start failure
            }
        case "Stop":
            audioRecorder?.stop()
            record_state = "Play"
            print("Stop")
        case "Play":
            if let player = try? AVAudioPlayer(contentsOf: audioRecorder!.url) {
                audioPlayer = player
                audioPlayer?.delegate = self
                audioPlayer?.play()
                record_state = "Record"
                print("Play")
            }
        default:
            print("broke000")
            print(record_state)
            break
        }
    }
    
    // Implement AVAudioPlayerDelegate methods to handle playback completion
    func audioPlayerDidFinishPlaying(_ player: AVAudioPlayer, successfully flag: Bool) {
        if flag {
            record_state = "Record"
            print("Finished playing")
            // Send the audio file to the server
            sendAudioFileThenDelete()
        }
    }

   func sendAudioFileThenDelete() {
       guard let audioURL = audioRecorder?.url else { return }
       print(audioURL)
       let url = URL(string: "\(base_url)/upload_audio")! // Ensure this URL is correct
       var request = URLRequest(url: url)
       request.httpMethod = "POST"
       
       let boundary = "Boundary-\(UUID().uuidString)"
       request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
       
       var body = Data()
       
       // Add the text part
       let message = "This is a test message with audio."
       body.append("--\(boundary)\r\n".data(using: .utf8)!)
       body.append("Content-Disposition: form-data; name=\"message\"\r\n\r\n".data(using: .utf8)!)
       body.append("\(message)\r\n".data(using: .utf8)!)
       
       // Add the audio file part
       do {
           let audioData = try Data(contentsOf: audioURL)
           body.append("--\(boundary)\r\n".data(using: .utf8)!)
           body.append("Content-Disposition: form-data; name=\"audio\"; filename=\"\(audioURL.lastPathComponent)\"\r\n".data(using: .utf8)!)
           body.append("Content-Type: audio/mpeg\r\n\r\n".data(using: .utf8)!)
           body.append(audioData)
           body.append("\r\n".data(using: .utf8)!)
       } catch {
           print("Failed to load audio file")
           return
       }
       
       body.append("--\(boundary)--\r\n".data(using: .utf8)!)
       
       request.httpBody = body
       
       let task = URLSession.shared.dataTask(with: request) { data, response, error in
           if let error = error {
               print("Error sending audio file: \(error.localizedDescription)")
               return
           }
           
           guard let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 else {
               print("Failed to send message and audio: \(String(describing: response))")
               return
           }
           
           if let data = data, let responseString = String(data: data, encoding: .utf8) {
               print("Server response: \(responseString)")
           }
       }
       
       task.resume()
   }
    
    @IBOutlet var sceneView: ARSCNView!
    
    @IBAction func test_send(_ sender: Any) {
        let urlString = "https://97b7-140-117-193-178.ngrok-free.app/post"
        guard let url = URL(string: urlString) else { return }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body: [String: Any] = ["message": "hey I am IPADDDDDDDD"]
        let bodyData = try? JSONSerialization.data(withJSONObject: body, options: [])
        
        request.httpBody = bodyData
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            guard let data = data, error == nil else {
                print(error?.localizedDescription ?? "No data")
                return
            }
            
            let responseJSON = try? JSONSerialization.jsonObject(with: data, options: [])
            if let responseJSON = responseJSON as? [String: Any] {
                print(responseJSON)
            }
        }.resume()
    }
    @IBAction func fetchMessageFromServer(_ sender: UIButton) {
        // Define the URL of the server
        guard let url = URL(string: "https://97b7-140-117-193-178.ngrok-free.app/get") else { return }
        
        // Create a URLSession data task to fetch data from the server's URL
        let task = URLSession.shared.dataTask(with: url) { (data, response, error) in
            // Ensure there is no error for this HTTP response
            guard error == nil else {
                print("Error: \(error!.localizedDescription)")
                return
            }
            
            // Ensure there is data returned from this HTTP response
            guard let content = data else {
                print("No data")
                return
            }
            
            // Serialize the data into an object
            do {
                if let json = try JSONSerialization.jsonObject(with: content, options: []) as? [String: Any],
                   let message = json["response"] as? String {
                    DispatchQueue.main.async {
                        // Use the message from the server
                        print("Message from server: \(message)")
                        // If you have a UILabel to display this message, update it
                        
                    }
                }
            } catch {
                print("Failed to convert data to JSON")
            }
        }
        task.resume()
    }

    @IBAction func right_pressed(_ sender: Any) {
            // Define the movement to the right. Adjust the '0.1' value to control the distance
            let moveRight = SCNAction.moveBy(x: 0.01, y: 0, z: 0, duration: 0.1)
            
            // Apply the movement action to the tank node
            tankNode?.runAction(moveRight)
    }
    
    @IBAction func left_pressed(_ sender: Any) {
        let moveLeft = SCNAction.moveBy(x: -0.01, y: 0, z: 0, duration: 0.1)
        tankNode?.runAction(moveLeft)
    }
    
    @IBAction func forward_pressed(_ sender: Any) {
        let moveForward = SCNAction.moveBy(x: 0, y: 0, z: -0.01, duration: 0.1)
        tankNode?.runAction(moveForward)
    }
    
    @IBAction func right_turn_pressed(_ sender: Any) {
        let rotateRight = SCNAction.rotateBy(x: 0, y: -CGFloat.pi / 16, z: 0, duration: 0.1)
        tankNode?.runAction(rotateRight)
    }
    
    @IBAction func left_turn_pressed(_ sender: Any) {
        let rotateLeft = SCNAction.rotateBy(x: 0, y: CGFloat.pi / 16, z: 0, duration: 0.1)
        tankNode?.runAction(rotateLeft)
    }
    
    @IBAction func fire_pressed(_ sender: Any) {
        if let fireSound = SCNAudioSource(named: "art.scnassets/cannon.mp3") {
            fireSound.load()
            let playSound = SCNAction.playAudio(fireSound, waitForCompletion: false)
            tankNode?.runAction(playSound)
        }
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        setupAudioRecorder()
        // Set the view's delegate
        sceneView.delegate = self
        
        // Show statistics such as fps and timing information
        sceneView.showsStatistics = true
        
        if let scene = SCNScene(named: "art.scnassets/TinyToyTank.usda") {
            // Set the scene to the view
            sceneView.scene = scene
            
            let tankParentNode = SCNNode()
            tankParentNode.name = "tankParentNode"

            // Assuming your tank parts are correctly identified (e.g., "tankBody", "tankTurret", etc.)
            if let tankBody =           sceneView.scene.rootNode.childNode(withName: "Sphere", recursively: true),

               let tankTurret = sceneView.scene.rootNode.childNode(withName: "Sphere_2", recursively: true) {
                // Remove the nodes from their current parent and add them to the tankParentNode
                tankBody.removeFromParentNode()
                tankTurret.removeFromParentNode()

                tankParentNode.addChildNode(tankBody)
                tankParentNode.addChildNode(tankTurret)
                tankParentNode.addChildNode(tankTurret)

                // Finally, add the tankParentNode to the scene's rootNode
                
                sceneView.scene.rootNode.addChildNode(tankParentNode)
                tankNode = sceneView.scene.rootNode.childNode(withName: "tankParentNode", recursively: true)
            }

        } else {
            print("Failed to load TinyToyTank.usda")
        }

    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        
        // Create a session configuration
        let configuration = ARWorldTrackingConfiguration()

        // Run the view's session
        sceneView.session.run(configuration)
    }
    
    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        
        // Pause the view's session
        sceneView.session.pause()
    }

    // MARK: - ARSCNViewDelegate
    
/*
    // Override to create and configure nodes for anchors added to the view's session.
    func renderer(_ renderer: SCNSceneRenderer, nodeFor anchor: ARAnchor) -> SCNNode? {
        let node = SCNNode()
     
        return node
    }
*/
    
    func session(_ session: ARSession, didFailWithError error: Error) {
        // Present an error message to the user
        
    }
    
    func sessionWasInterrupted(_ session: ARSession) {
        // Inform the user that the session has been interrupted, for example, by presenting an overlay
        
    }
    
    func sessionInterruptionEnded(_ session: ARSession) {
        // Reset tracking and/or remove existing anchors if consistent tracking is required
        
    }
}


