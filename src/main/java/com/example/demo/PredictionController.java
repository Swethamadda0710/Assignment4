package com.example.demo;

import java.io.File;
import java.io.IOException;

import org.springframework.core.io.FileSystemResource;
import org.springframework.http.*;
import org.springframework.stereotype.Controller;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

@Controller
public class PredictionController {

    @PostMapping("/predict")
    @ResponseBody
    public PredictionResponse predict(@RequestParam("image") MultipartFile image)
            throws IOException {

        // Save uploaded image temporarily
        File tempFile = File.createTempFile("upload", image.getOriginalFilename());
        image.transferTo(tempFile);

        RestTemplate restTemplate = new RestTemplate();

        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("image", new FileSystemResource(tempFile));

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);

        HttpEntity<MultiValueMap<String, Object>> requestEntity =
                new HttpEntity<>(body, headers);

        // Call Flask API deployed on Render
        ResponseEntity<PredictionResponse> response =
                restTemplate.postForEntity(
                        "https://assignment4-1z9q.onrender.com/predict",
                        requestEntity,
                        PredictionResponse.class);

        // Delete temporary file
        tempFile.delete();

        return response.getBody();
    }
}